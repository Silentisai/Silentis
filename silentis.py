# silentis.py
import os
import sys
from pathlib import Path
import json
import requests
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from llama_cpp import Llama
import psutil
from threading import Lock
import threading

class ConfigManager:
    def __init__(self):
        self.app_path = Path(__file__).parent
        self.config_file = self.app_path / "config.json"
        self.supported_models = {
            1: {"name": "Reasoner v1", "ram_required": 8, "url": "https://huggingface.co/Qwen/Qwen2.5-Coder-7B-Instruct-GGUF/resolve/main/qwen2.5-coder-7b-instruct-q4_0.gguf?download=true"},
            2: {"name": "Llama 3 8B Instruct", "ram_required": 8, "url": "https://huggingface.co/QuantFactory/Meta-Llama-3-8B-Instruct-GGUF/resolve/main/Meta-Llama-3-8B-Instruct.Q4_K_M.gguf?download=true"},
            3: {"name": "DeepSeek-R1-Distill-Qwen-7B", "ram_required": 8, "url": "https://huggingface.co/unsloth/DeepSeek-R1-Distill-Qwen-7B-GGUF/resolve/main/DeepSeek-R1-Distill-Qwen-7B-Q4_K_M.gguf?download=true"},
            4: {"name": "Phi-3 Mini Instruct", "ram_required": 4, "url": "https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/resolve/main/Phi-3-mini-4k-instruct-q4.gguf?download=true"}
        }
        self.default_config = {
            "system_prompt": "You are Silentis, a helpful AI assistant. Answer briefly and accurately.",
            "instructions": "",
            "model_params": {"temp": 0.7, "max_tokens": 50, "top_p": 0.9},
            "use_gpu": False,
            "selected_model": None,
            "show_welcome": True,
            "disable_model_selection": False,
            "api_enabled": False,
            "api_host": "0.0.0.0",
            "api_port": 5000
        }

    def load_config(self):
        try:
            if self.config_file.exists():
                with open(self.config_file, "r") as f:
                    return {**self.default_config, **json.load(f)}
            return self.default_config
        except Exception as e:
            print(f"Loading default config due to error: {str(e)}")
            return self.default_config

    def save_config(self, config):
        try:
            with open(self.config_file, "w") as f:
                json.dump(config, f, indent=2)
            print("Configuration saved successfully.")
            return True
        except Exception as e:
            print(f"Failed to save config: {str(e)}")
            return False

class AICore:
    def __init__(self, model_path, config):
        self.model_path = model_path
        self.config = config
        self.model = None
        self.chat_history = []
        self.lock = Lock()
        self.load_model()
        self.update_system_prompt()

    def check_system_requirements(self, model_info):
        available_ram = psutil.virtual_memory().available / (1024 ** 3)
        required_ram = model_info["ram_required"]
        if available_ram < required_ram:
            raise RuntimeError(f"Insufficient RAM: {model_info['name']} requires {required_ram}GB, only {available_ram:.1f}GB available")

    def update_system_prompt(self):
        base_prompt = self.config.get("system_prompt", "You are Silentis, a helpful AI assistant.")
        instructions = self.config.get("instructions", "")
        model_name = Path(self.model_path).stem.lower()
        if "reasoner" in model_name:
            self.system_prompt = f"{base_prompt} Focus on reasoning.\n{instructions}"
        elif "llama" in model_name:
            self.system_prompt = f"{base_prompt} Excel at instructions.\n{instructions}"
        elif "deepseek" in model_name:
            self.system_prompt = f"{base_prompt} Provide deep insights.\n{instructions}"
        elif "phi-3" in model_name:
            self.system_prompt = f"{base_prompt} Keep it quick and simple.\n{instructions}"
        else:
            self.system_prompt = f"{base_prompt}\n{instructions}"
        self.chat_history = [{"role": "system", "content": self.system_prompt}]

    def load_model(self):
        if not Path(self.model_path).exists():
            raise FileNotFoundError(f"Model file not found at {self.model_path}")
        n_gpu_layers = -1 if self.config['use_gpu'] else 0
        self.model = Llama(
            model_path=str(self.model_path),
            n_ctx=512,
            n_threads=max(1, os.cpu_count() // 2),
            n_gpu_layers=n_gpu_layers,
            verbose=False
        )

    def generate_response(self, prompt):
        with self.lock:
            self.chat_history.append({"role": "user", "content": prompt})
            full_prompt = "\n".join([f"<|system|>{entry['content']}\n" if entry['role'] == 'system'
                                   else f"<|user|>{entry['content']}\n"
                                   for entry in self.chat_history]) + "\n<|assistant|>"
            try:
                response = self.model(
                    full_prompt,
                    temperature=self.config['model_params']['temp'],
                    max_tokens=self.config['model_params']['max_tokens'],
                    top_p=self.config['model_params']['top_p'],
                    echo=False,
                    stop=["\n"]
                )
                output = response['choices'][0]['text'].strip()
                self.chat_history.append({"role": "assistant", "content": output})
                return output
            except Exception as e:
                raise RuntimeError(f"Generation error: {str(e)}")

    def __del__(self):
        if self.model:
            self.model = None

class Silentis:
    def __init__(self):
        self.cfg = ConfigManager()
        self.config = self.cfg.load_config()
        self.ai = None
        self.app = Flask(__name__)
        CORS(self.app)
        self.setup_api_routes()
        self.setup_html_route()

    def download_model(self, model_number):
        if model_number not in self.cfg.supported_models:
            print(f"Invalid model number. Choose from: {list(self.cfg.supported_models.keys())}")
            return None
        model_info = self.cfg.supported_models[model_number]
        model_filename = Path(model_info['url']).name.split('?')[0]
        model_path = self.cfg.app_path / model_filename
        if not model_path.exists():
            print(f"Downloading {model_info['name']}...")
            try:
                response = requests.get(model_info['url'], stream=True, timeout=30)
                response.raise_for_status()
                with open(model_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"Downloaded {model_info['name']} to {model_path}")
            except Exception as e:
                print(f"Download failed: {str(e)}")
                return None
        return model_path

    def load_model(self, model_number=None):
        if model_number is None:
            model_number = self.config.get('selected_model')
            if model_number is None:
                print("No default model selected. Please select a model first.")
                return
        model_info = self.cfg.supported_models.get(model_number)
        if not model_info:
            print(f"Invalid model number. Choose from: {list(self.cfg.supported_models.keys())}")
            return
        try:
            self.check_system_requirements(model_info)
        except RuntimeError as e:
            print(str(e))
            return
        model_path = self.download_model(model_number)
        if model_path:
            self.config['selected_model'] = model_number
            self.cfg.save_config(self.config)
            self.ai = AICore(model_path, self.config)
            print(f"Loaded {model_info['name']} successfully")

    def check_system_requirements(self, model_info):
        available_ram = psutil.virtual_memory().available / (1024 ** 3)
        required_ram = model_info["ram_required"]
        if available_ram < required_ram:
            raise RuntimeError(f"Insufficient RAM: {model_info['name']} requires {required_ram}GB, only {available_ram:.1f}GB available")

    def _get_valid_input(self, prompt, input_type, min_val=None, max_val=None):
        while True:
            value = input(prompt)
            if not value:
                if 'Temperature' in prompt:
                    return self.config['model_params']['temp']
                elif 'Max Tokens' in prompt:
                    return self.config['model_params']['max_tokens']
                elif 'Top-P' in prompt:
                    return self.config['model_params']['top_p']
                elif 'Port' in prompt:
                    return self.config['api_port']
            try:
                num = input_type(value)
                if (min_val is None or num >= min_val) and (max_val is None or num <= max_val):
                    return num
                print(f"Value must be between {min_val} and {max_val}")
            except ValueError:
                print(f"Invalid {input_type.__name__} value")

    def _show_welcome(self):
        print(r"""
 ______     __     __         ______     __   __     ______   __     ______    
/\  ___\   /\ \   /\ \       /\  ___\   /\ "-.\ \   /\__  _\ /\ \   /\  ___\   
\ \___  \  \ \ \  \ \ \____  \ \  __\   \ \ \-.  \  \/_/\ \/ \ \ \  \ \___  \  
 \/\_____\  \ \_\  \ \_____\  \ \_____\  \ \_\\"\_\    \ \_\  \ \_\  \/\_____\ 
  \/_____/   \/_/   \/_____/   \/_____/   \/_/ \/_/     \/_/   \/_/   \/_____/ 
        """)
        print("Silentis AI - Python Plugin")
        print("Developed by: Silentis Team")
        print("MIT License | Version 1.2.3")
        print("-------------------------------------------")
        print("Documentation: https://silentis.ai/")
        print("Website: https://silentis.ai")
        print("Github: https://github.com/Silentisai")
        print("-------------------------------------------")
        print("X: https://x.com/silentisproject")
        print("Telegram: https://t.me/SilentisAi")
        print("===========================================")
        print("Support our mission: https://springboard.pancakeswap.finance/bsc/token/0x8a87562947422db0eb3070a5a1ac773c7a8d64e7")
        print("===========================================")

    def _show_model_list(self):
        print("\n--- Available Models ---")
        model_desc = {
            'Reasoner': 'Advanced reasoning & logic',
            'Llama': 'Instruction execution specialist',
            'DeepSeek': 'Deep analysis & insights',
            'Phi-3': 'Lightweight quick responses'
        }
        for num, info in self.cfg.supported_models.items():
            model_type = info['name'].split()[0]
            desc = model_desc.get(model_type, 'General purpose model')
            ram = info['ram_required']
            print(f"[{num}] {info['name']} ({ram}GB RAM) - {desc}")

    def start_chat(self):
        if not self.ai:
            print("No model loaded. Please load a model from Settings first.")
            return
        print("\n--- Chat Started ---")
        print("Type 'quit' to return to main menu.")
        while True:
            prompt = input("> ").strip()
            if prompt.lower() == 'quit':
                print("Returning to main menu...")
                break
            try:
                sys.stdout.write("Thinking...\r")
                sys.stdout.flush()
                response = self.ai.generate_response(prompt)
                sys.stdout.write("\r" + " " * 20 + "\r")
                print(f"Assistant: {response}")
            except Exception as e:
                sys.stdout.write("\r" + " " * 20 + "\r")
                print(f"Error: {str(e)}")

    def settings_menu(self):
        while True:
            print("\n--- Settings Menu ---")
            print("1: Load Model")
            print("2: Update Model Parameters")
            print("0: Back to Main Menu")
            choice = input("Enter your choice: ").strip()
            if choice == '0':
                break
            elif choice == '1':
                self._show_model_list()
                model_choice = input("Enter the number of the model to load (or 'back' to return): ").strip()
                if model_choice.lower() == 'back':
                    continue
                if model_choice in ['1', '2', '3', '4']:
                    self.load_model(int(model_choice))
                else:
                    print("Invalid choice. Please try again.")
            elif choice == '2':
                print("\n--- Update Model Parameters ---")
                print(f"Current settings: Temp={self.config['model_params']['temp']}, "
                      f"Max Tokens={self.config['model_params']['max_tokens']}, "
                      f"Top-P={self.config['model_params']['top_p']}, "
                      f"GPU={'Enabled' if self.config['use_gpu'] else 'Disabled'}, "
                      f"Show Welcome={'Enabled' if self.config['show_welcome'] else 'Disabled'}, "
                      f"Disable Model Selection={'Enabled' if self.config['disable_model_selection'] else 'Disabled'}, "
                      f"API={'Enabled' if self.config['api_enabled'] else 'Disabled'}, "
                      f"API Host={self.config['api_host']}, "
                      f"API Port={self.config['api_port']}, "
                      f"Instructions='{self.config['instructions']}'")
                try:
                    temp = self._get_valid_input("Enter Temperature (0-1, default 0.7): ", float, 0.0, 1.0)
                    max_tokens = self._get_valid_input("Enter Max Tokens (1-1000, default 50): ", int, 1, 1000)
                    top_p = self._get_valid_input("Enter Top-P (0-1, default 0.9): ", float, 0.0, 1.0)
                    use_gpu = input("Enable GPU? (y/n, default No): ").lower() in ['y', 'yes']
                    show_welcome = input("Show Welcome Message? (y/n, default Yes): ").lower() not in ['n', 'no']
                    disable_model_selection = input("Disable Model Selection? (y/n, default No): ").lower() in ['y', 'yes']
                    api_enabled = input("Enable API? (y/n, default No): ").lower() in ['y', 'yes']
                    api_host = input(f"API Host (default {self.config['api_host']}): ") or self.config['api_host']
                    api_port = self._get_valid_input(f"API Port (1-65535, default {self.config['api_port']}): ", int, 1, 65535)
                    instructions = input("Enter Instructions (or press Enter to keep current): ") or self.config['instructions']

                    if disable_model_selection and not self.config['selected_model']:
                        print("Please select a default model:")
                        self._show_model_list()
                        default_model = input("Enter the number of the default model: ").strip()
                        if default_model.isdigit() and int(default_model) in self.cfg.supported_models:
                            self.config['selected_model'] = int(default_model)
                            print(f"Default model set to: {self.cfg.supported_models[int(default_model)]['name']}")
                        else:
                            print("Invalid model number. Disabling model selection has been canceled.")
                            disable_model_selection = False

                    self.config['model_params']['temp'] = temp
                    self.config['model_params']['max_tokens'] = max_tokens
                    self.config['model_params']['top_p'] = top_p
                    self.config['use_gpu'] = use_gpu
                    self.config['show_welcome'] = show_welcome
                    self.config['disable_model_selection'] = disable_model_selection
                    self.config['api_enabled'] = api_enabled
                    self.config['api_host'] = api_host
                    self.config['api_port'] = api_port
                    self.config['instructions'] = instructions
                    self.cfg.save_config(self.config)
                    if self.ai:
                        self.ai.config = self.config
                        self.ai.update_system_prompt()
                    print("Settings updated. Restart model for GPU changes to take effect.")
                except Exception as e:
                    print(f"Error updating settings: {str(e)}")
            else:
                print("Invalid choice. Please try again.")

    def setup_api_routes(self):
        @self.app.route('/api/models', methods=['GET'])
        def get_models():
            return jsonify(self.cfg.supported_models)

        @self.app.route('/api/load_model', methods=['POST'])
        def load_model_route():
            data = request.get_json()
            if not data or 'model_number' not in data:
                return jsonify({'error': 'Model number required'}), 400
            model_number = int(data['model_number'])
            if model_number not in self.cfg.supported_models:
                return jsonify({'error': 'Invalid model number'}), 400
            self.load_model(model_number)
            if self.ai:
                return jsonify({'message': f"Loaded {self.cfg.supported_models[model_number]['name']} successfully"})
            return jsonify({'error': 'Failed to load model'}), 500

        @self.app.route('/api/chat', methods=['POST'])
        def chat():
            if not self.ai:
                return jsonify({'error': 'No model loaded'}), 400
            data = request.get_json()
            if not data or 'prompt' not in data:
                return jsonify({'error': 'Prompt required'}), 400
            try:
                response = self.ai.generate_response(data['prompt'])
                return jsonify({'response': response})
            except Exception as e:
                return jsonify({'error': str(e)}), 500

        @self.app.route('/api/config', methods=['GET'])
        def get_config():
            return jsonify(self.config)

        @self.app.route('/api/config', methods=['POST'])
        def update_config():
            data = request.get_json()
            if not data:
                return jsonify({'error': 'Config data required'}), 400
            self.config.update(data)
            if self.cfg.save_config(self.config):
                if self.ai:
                    self.ai.config = self.config
                    self.ai.update_system_prompt()
                return jsonify({'message': 'Config updated successfully'})
            return jsonify({'error': 'Failed to save config'}), 500

        @self.app.route('/api/status', methods=['GET'])
        def status():
            return jsonify({
                'model_loaded': bool(self.ai),
                'selected_model': self.config.get('selected_model'),
                'available_ram': psutil.virtual_memory().available / (1024 ** 3)
            })

    def setup_html_route(self):
        @self.app.route('/')
        def serve_html():
            return send_from_directory(self.cfg.app_path, 'silentis.html')

    def start_api(self):
        if self.config['api_enabled']:
            print(f"Starting API server on {self.config['api_host']}:{self.config['api_port']}")
            threading.Thread(
                target=self.app.run,
                args=(self.config['api_host'], self.config['api_port']),
                kwargs={'threaded': True},
                daemon=True
            ).start()

    def run(self):
        if self.config.get('show_welcome', True):
            self._show_welcome()
        
        self.start_api()

        if self.config.get('disable_model_selection', False) and self.config.get('selected_model'):
            self.load_model()
            if self.ai:
                self.start_chat()
        else:
            while True:
                print("\n--- Main Menu ---")
                print("1: Chat")
                print("2: Settings")
                print("0: Exit")
                choice = input("Enter your choice: ").strip()
                if choice == '0':
                    print("Exiting Silentis AI...")
                    break
                elif choice == '1':
                    self.start_chat()
                elif choice == '2':
                    self.settings_menu()
                else:
                    print("Invalid choice. Please try again.")

if __name__ == "__main__":
    plugin = Silentis()
    plugin.run()
