# Silentis AI - Core

<p align="center">
  <img src="https://silentis.ai/SilentisAiGit.png?raw=true">
</p>

**Silentis Open Source Core Python Plugin**  
**MIT License | Version 1.0**  

A flexible AI plugin system for interacting with multiple large language models, featuring:  
✅ **Multi-model support** (Reasoner, Llama, DeepSeek, Phi-3)  
✅ **GPU acceleration** toggle  
✅ **Customizable parameters** (temperature, max tokens, Top-P, system prompt, instructions)  
✅ **RAM requirement checks**  
✅ **Persistent configuration**  
✅ **Interactive chat interface** (terminal and web-based)  
✅ **Web API** for browser interaction  

---

## Features

- 🤖 **Supported Models**:  
  - `Reasoner v1` (8GB RAM) - Advanced reasoning  
  - `Llama 3 8B Instruct` (8GB RAM) - Instruction specialist  
  - `DeepSeek-R1-Distill-Qwen-7B` (8GB RAM) - Deep insights  
  - `Phi-3 Mini Instruct` (4GB RAM) - Lightweight responses  

- ⚙️ **Configurable Parameters**:  
  - Temperature (0-1)  
  - Max output tokens (1-1000)  
  - Top-P probability  
  - System Prompt  
  - Instructions (persistent AI behavior customization)  
  - GPU usage toggle  
  - API settings (host, port, enable/disable)  

- 🌐 **Web Interface**:  
  - Multi-page layout (Chat, Settings, Status)  
  - Accessible at `http://localhost:5000` when API is enabled  

---

## Installation

1. Clone the repository:  
   ```bash
   git clone https://github.com/silentisai/silentis.git
   cd silentis
   ```

2. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```
   *Note*: Ensure you have `llama-cpp-python`, `flask`, `flask-cors`, `requests`, and `psutil` installed. Create a `requirements.txt` with:
   ```
   llama-cpp-python
   flask
   flask-cors
   requests
   psutil
   ```

3. (Optional) Configure GPU support:  
   ```bash
   # Install CUDA toolkit for GPU acceleration
   # Follow instructions at https://developer.nvidia.com/cuda-downloads
   # Then install llama-cpp-python with GPU support:
   pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu121
   ```

4. Ensure `index.html` is in the same directory as `silentis.py`.

---

## Usage

### Terminal Interface

1. Run the plugin:  
   ```bash
   python silentis.py
   ```

2. If `show_welcome` is enabled (default), you’ll see the welcome message:
   ```
   ______     __     __         ______     __   __     ______   __     ______
   /\  ___\   /\ \   /\ \       /\  ___\   /\ "-.\ \   /\__  _\ /\ \   /\  ___\   
   \ \___  \  \ \ \  \ \ \____  \ \  __\   \ \ \-.  \  \/_/\ \/ \ \ \  \ \___  \  
    \/\_____\  \ \_\  \ \_____\  \ \_____\  \ \_\\"\_\    \ \_\  \ \_\  \/\_____\ 
     \/_____/   \/_/   \/_____/   \/_____/   \/_/ \/_/     \/_/   \/_/   \/_____/ 
   Silentis AI - Python Plugin
   Developed by: Silentis Team
   MIT License | Version 1.0
   ...
   ```

3. **Main Menu** (if `disable_model_selection` is `False`):
   ```
   --- Main Menu ---
   1: Chat
   2: Settings
   0: Exit
   Enter your choice:
   ```
   - **1: Chat**: Start an interactive chat session with the loaded model. Type `quit` to return to the menu.
   - **2: Settings**: Configure models and parameters (see below).
   - **0: Exit**: Close the plugin.

4. **Settings Menu**:
   ```
   --- Settings Menu ---
   1: Load Model
   2: Update Model Parameters
   0: Back to Main Menu
   ```
   - **1: Load Model**: Choose a model to download and load.
   - **2: Update Model Parameters**: Adjust settings like temperature, max tokens, instructions, etc.

5. **Direct Chat Mode** (if `disable_model_selection` is `True` and a model is selected):
   - Loads the default model and starts the chat immediately.

6. Example Chat:
   ```
   --- Chat Started ---
   Type 'quit' to return to main menu.
   > Hello, how are you?
   Thinking...
   Assistant: I'm Silentis, doing great! How can I assist you today?
   > quit
   Returning to main menu...
   ```

### Web Interface (API Mode)

1. Enable the API:
   - Edit `config.json` to set `"api_enabled": true` (or use the Settings menu in the terminal).
   - Default host: `0.0.0.0`, port: `5000`.

2. Run the plugin:  
   ```bash
   python silentis.py
   ```
   - You’ll see: `Starting API server on 0.0.0.0:5000`.

3. Open your browser and navigate to:  
   ```
   http://localhost:5000
   ```

4. **Web Interface Layout**:
   - **Sidebar**:  
     - Chat (default page)  
     - Settings  
     - Status  
   - **Chat Page**:  
     - Chat window to send prompts and view responses.  
     - Enter a prompt and click "Send".  
   - **Settings Page**:  
     - **Available Models**: List supported models.  
     - **Load Model**: Select and load a model.  
     - **Configuration**: Adjust temperature, max tokens, Top-P, system prompt, and instructions. Click "Apply Config" to save.  
   - **Status Page**:  
     - Check model status, selected model, and available RAM.

5. Example Web Interaction:
   - Go to "Settings", set "Instructions" to "Act as a coding assistant", and click "Apply Config".
   - Switch to "Chat", type "Write a Python function", and see a code-focused response.

---

## Configuration

Modify `config.json` or use the terminal/web settings to customize Silentis AI. Changes persist across sessions.

### Available Settings

| Setting                  | Description                                      | Range/Options           | Default                |
|--------------------------|--------------------------------------------------|-------------------------|------------------------|
| `system_prompt`          | Base prompt for AI behavior                     | Text                    | "You are Silentis..."  |
| `instructions`           | Additional instructions for AI behavior         | Text                    | ""                     |
| `model_params.temp`      | Response randomness                             | 0.0 - 1.0              | 0.7                    |
| `model_params.max_tokens`| Max response length                             | 1 - 1000               | 50                     |
| `model_params.top_p`     | Token probability threshold                     | 0.0 - 1.0              | 0.9                    |
| `use_gpu`                | Enable GPU acceleration                         | True/False             | False                  |
| `selected_model`         | Default model number                            | 1, 2, 3, 4, or null    | null                   |
| `show_welcome`           | Show welcome message on start                   | True/False             | True                   |
| `disable_model_selection`| Skip model selection on start                   | True/False             | False                  |
| `api_enabled`            | Enable web API                                  | True/False             | False                  |
| `api_host`               | API server host                                 | IP address             | "0.0.0.0"              |
| `api_port`               | API server port                                 | 1 - 65535              | 5000                   |

### Terminal Configuration Example
```
--- Update Model Parameters ---
Current settings: Temp=0.7, Max Tokens=50, Top-P=0.9, GPU=Disabled, Show Welcome=Enabled, ...
Enter Temperature (0-1, default 0.7): 0.8
Enter Max Tokens (1-1000, default 50): 100
Enter Top-P (0-1, default 0.9): 
Enable GPU? (y/n, default No): n
Show Welcome Message? (y/n, default Yes): y
Disable Model Selection? (y/n, default No): y
Please select a default model:
[1] Reasoner v1 (8GB RAM) - Advanced reasoning & logic
...
Enter the number of the default model: 2
Default model set to: Llama 3 8B Instruct
API Enabled? (y/n, default No): y
API Host (default 0.0.0.0): 
API Port (1-65535, default 5000): 
Enter Instructions (or press Enter to keep current): Act as a coding assistant
Settings updated. Restart model for GPU changes to take effect.
```

### Web Configuration
- Navigate to `http://localhost:5000`, click "Settings" in the sidebar, and adjust values under "Configuration". Click "Apply Config" to save.

---

## API Endpoints

When `api_enabled` is `True`, the following endpoints are available at `http://localhost:5000/api/`:

| Endpoint          | Method | Description                        | Request Body Example                          | Response Example                              |
|-------------------|--------|------------------------------------|----------------------------------------------|----------------------------------------------|
| `/models`         | GET    | List supported models             | -                                            | `{"1": {"name": "Reasoner v1", ...}, ...}`   |
| `/load_model`     | POST   | Load a model                      | `{"model_number": 2}`                        | `{"message": "Loaded Llama 3 8B..."}`        |
| `/chat`           | POST   | Send a chat prompt                | `{"prompt": "Hello"}`                        | `{"response": "Hi there!"}`                  |
| `/config`         | GET    | Get current config                | -                                            | `{"system_prompt": "...", "instructions": "..."}` |
| `/config`         | POST   | Update config                     | `{"model_params": {"temp": 0.8}, "instructions": "Code assistant"}` | `{"message": "Config updated successfully"}` |
| `/status`         | GET    | Check system status               | -                                            | `{"model_loaded": true, "available_ram": 16.2}` |

---

## Knowledge Base

The plugin downloads models from HuggingFace. Below are the supported models:

| Model Name               | RAM Required | Description                          |
|--------------------------|--------------|--------------------------------------|
| Reasoner v1              | 8GB          | Advanced reasoning and logic         |
| Llama 3 8B Instruct      | 8GB          | Instruction execution specialist     |
| DeepSeek-R1-Distill-Qwen | 8GB          | Deep analysis and insights           |
| Phi-3 Mini Instruct      | 4GB          | Lightweight quick responses          |

---

## Acknowledgments

- Model weights from [HuggingFace](https://huggingface.co)  
- Powered by [llama-cpp-python](https://github.com/abetlen/llama-cpp-python)  
- Web framework: [Flask](https://flask.palletsprojects.com/)  

> **Note**: Ensure sufficient RAM (4GB or 8GB depending on the model). GPU support requires CUDA setup.

---

## License

MIT License  
Copyright (c) 2025 - Silentis AI

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---

### Notes for Deployment
- Rename `silentis.html` to `index.html` in your project directory to match the provided code.
- Update the GitHub repository URL in the README if it changes.
- Ensure all links (e.g., `https://silentis.ai`) are valid or replace them with placeholders if not yet live.

This README provides a comprehensive guide for users to set up and use Silentis AI via both the terminal and the web interface at `localhost:5000`. Let me know if you need further adjustments!
