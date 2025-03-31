import os
import sys
from pathlib import Path
import json
import requests
from llama_cpp import Llama
import psutil


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
            "model_params": {"temp": 0.7, "max_tokens": 50, "top_p": 0.9},
            "use_gpu": False,
            "selected_model": None,
            "show_welcome": True,
            "disable_model_selection": False  # New key for disabling model selection
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
        except Exception as e:
            print(f"Failed to save config: {str(e)}")


class AICore:
    def __init__(self, model_path, config):
        self.model_path = model_path
        self.config = config
        self.model = None
        self.chat_history = []
        self.load_model()
        self.update_system_prompt()

    def check_system_requirements(self, model_info):
        available_ram = psutil.virtual_memory().available / (1024 ** 3)
        required_ram = model_info["ram_required"]
        if available_ram < required_ram:
            raise RuntimeError(f"Insufficient RAM: {model_info['name']} requires {required_ram}GB, only {available_ram:.1f}GB available")

    def update_system_prompt(self):
        base_prompt = "You are Silentis, a helpful AI assistant."
        model_name = Path(self.model_path).stem.lower()
        if "reasoner" in model_name:
            self.system_prompt = f"{base_prompt} Focus on reasoning."
        elif "llama" in model_name:
            self.system_prompt = f"{base_prompt} Excel at instructions."
        elif "deepseek" in model_name:
            self.system_prompt = f"{base_prompt} Provide deep insights."
        elif "phi-3" in model_name:
            self.system_prompt = f"{base_prompt} Keep it quick and simple."
        else:
            self.system_prompt = base_prompt
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

    def update_model_settings(self):
        print("\n--- Update Model Settings ---")
        print(f"Current settings: Temp={self.config['model_params']['temp']}, "
              f"Max Tokens={self.config['model_params']['max_tokens']}, "
              f"Top-P={self.config['model_params']['top_p']}, "
              f"GPU={'Enabled' if self.config['use_gpu'] else 'Disabled'}, "
              f"Show Welcome={'Enabled' if self.config['show_welcome'] else 'Disabled'}, "
              f"Disable Model Selection={'Enabled' if self.config['disable_model_selection'] else 'Disabled'}")
        try:
            temp = self._get_valid_input("Enter Temperature (0-1, default 0.7): ", float, 0.0, 1.0)
            max_tokens = self._get_valid_input("Enter Max Tokens (1-1000, default 50): ", int, 1, 1000)
            top_p = self._get_valid_input("Enter Top-P (0-1, default 0.9): ", float, 0.0, 1.0)
            use_gpu = input("Enable GPU? (y/n, default No): ").lower() in ['y', 'yes']
            show_welcome = input("Show Welcome Message? (y/n, default Yes): ").lower() not in ['n', 'no']
            disable_model_selection = input("Disable Model Selection? (y/n, default No): ").lower() in ['y', 'yes']

            if disable_model_selection:
                # Prompt user to select a default model
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
            self.config['disable_model_selection'] = disable_model_selection  # Save the new setting
            self.cfg.save_config(self.config)
            print("Settings updated. Restart model for GPU changes to take effect.")
        except Exception as e:
            print(f"Error updating settings: {str(e)}")

    def _get_valid_input(self, prompt, input_type, min_val=None, max_val=None):
        while True:
            value = input(prompt)
            if not value:
                return self.config['model_params'].get(prompt.split(' ')[1].lower(), None)
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
        print("MIT License | Version 1.0")
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

    def run(self):
        if self.config.get('show_welcome', True):  # Only show if enabled
            self._show_welcome()

        if self.config.get('disable_model_selection', False):
            # Skip model selection and load the default model
            if self.config.get('selected_model') is None:
                print("No default model selected. Please select a model first.")
                self.config['disable_model_selection'] = False
                self.cfg.save_config(self.config)
            else:
                self.load_model()
                if self.ai:
                    self.start_chat()
        else:
            while True:
                self._show_model_list()
                print("10: Configure model settings")
                print("0: Exit")
                choice = input("Enter your choice: ").strip()
                if choice == '0':
                    print("Exiting Silentis AI...")
                    break
                elif choice == '10':
                    self.update_model_settings()
                elif choice in ['1', '2', '3', '4']:
                    self.load_model(int(choice))
                    if self.ai:
                        self.start_chat()
                else:
                    print("Invalid choice. Please try again.")

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


if __name__ == "__main__":
    plugin = Silentis()
    plugin.run()