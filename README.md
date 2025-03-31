# Silentis AI - Core

<p align="center">
  <img src="https://silentis.ai/SilentisAiGit.png?raw=true">
</p>

**Silentis Open Source Core Python Plugin**  
**MIT License | Version 1.0**  

A flexible AI plugin system for interacting with multiple large language models, featuring:  
✅ **Multi-model support** (Reasoner, Llama, DeepSeek, Phi-3)  
✅ **GPU acceleration** toggle  
✅ **Customizable parameters** (temperature, max tokens, Top-P)  
✅ **RAM requirement checks**  
✅ **Persistent configuration**  
✅ **Interactive chat interface**  

---

## Features

- 🤖 **Supported Models**:  
  - `Reasoner v1` (8GB RAM) - Advanced reasoning  
  - `Llama 3 8B` (8GB) - Instruction specialist  
  - `DeepSeek-R1` (8GB) - Deep insights  
  - `Phi-3 Mini` (4GB) - Lightweight responses  

- ⚙️ **Configurable Parameters**:  
  - Temperature (0-1)  
  - Max output tokens (1-1000)  
  - Top-P probability  
  - GPU usage toggle  

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

3. (Optional) Configure GPU support:  
   ```bash
   # Install CUDA toolkit for GPU acceleration
   # Follow instructions at https://developer.nvidia.com/cuda-downloads
   ```

---

## Usage

1. Run the plugin:  
   ```bash
   python run.py
   ```

2. Follow the on-screen instructions:  
   ```text
   --- Main Menu ---
   [1] Reasoner v1 (8GB) - Advanced reasoning
   [2] Llama 3 8B (8GB) - Instruction specialist
   [3] DeepSeek-R1 (8GB) - Deep insights
   [4] Phi-3 Mini (4GB) - Lightweight responses
   10: Configure settings
   0: Exit
   ```

3. During chat:  
   - Type `quit` to return to the menu.  
   - The model shows "Thinking..." while generating responses.

---

---

## Configuration

Modify `config.json` or use the in-app settings menu (option `10`) to customize Silentis AI's behavior. All changes are saved automatically and persist across sessions.

### Accessing Settings
1. Run the plugin:
   ```bash
   python run.py
   ```
2. From the main menu, select `10: Configure model settings`.

### Available Settings

#### 1. **Temperature (`Temp`)**
   - **Description**: Controls the randomness of the model's responses. Lower values produce more deterministic outputs, while higher values encourage creativity.
   - **Range**: `0.0` to `1.0`
   - **Default**: `0.7`

#### 2. **Max Tokens (`Max Tokens`)**
   - **Description**: Sets the maximum number of tokens the model will generate in a single response. Higher values allow for longer responses but may increase processing time.
   - **Range**: `1` to `1000`
   - **Default**: `50`

#### 3. **Top-P Sampling (`Top-P`)**
   - **Description**: Determines the cumulative probability threshold for token selection. This parameter filters out low-probability tokens to maintain coherence in responses.
   - **Range**: `0.0` to `1.0`
   - **Default**: `0.9`

#### 4. **GPU Acceleration (`Enable GPU`)**
   - **Description**: Toggle GPU usage for faster inference. Requires CUDA-compatible hardware and drivers.
   - **Options**: `y` (Yes) / `n` (No)
   - **Default**: `No`

#### 5. **Show Welcome Message (`Show Welcome Message`)**
   - **Description**: Enable or disable the display of the welcome message when the plugin starts. Useful for reducing startup clutter.
   - **Options**: `y` (Yes) / `n` (No)
   - **Default**: `Yes`

#### 6. **Disable Model Selection (`Disable Model Selection`)**
   - **Description**: Skip the model selection menu on startup and directly load a default model. If enabled, you must select a default model during configuration.
   - **Options**: `y` (Yes) / `n` (No)
   - **Default**: `No`

   **Note**: When enabling this option, you will be prompted to select a default model from the available models. This ensures that the plugin always loads the same model without requiring manual selection each time.

### Example Interaction

Here’s how the settings menu works:

```text
--- Update Model Settings ---
Current settings: Temp=0.7, Max Tokens=50, Top-P=0.9, GPU=Disabled, Show Welcome=Enabled, Disable Model Selection=Disabled
Enter Temperature (0-1, default 0.7): 
Enter Max Tokens (1-1000, default 50): 100
Enter Top-P (0-1, default 0.9): 
Enable GPU? (y/n, default No): n
Show Welcome Message? (y/n, default Yes): y
Disable Model Selection? (y/n, default No): y
Please select a default model:
--- Available Models ---
[1] Reasoner v1 (8GB RAM) - Advanced reasoning & logic
[2] Llama 3 8B Instruct (8GB RAM) - Instruction execution specialist
[3] DeepSeek-R1-Distill-Qwen-7B (8GB RAM) - Deep analysis & insights
[4] Phi-3 Mini Instruct (4GB RAM) - Lightweight quick responses
Enter the number of the default model: 1
Default model set to: Reasoner v1
Settings updated. Restart model for GPU changes to take effect.
```

---

## Knowledge Base

The plugin supports downloading and using pre-trained models hosted on HuggingFace. Below are the supported models and their details:

| Model Name               | RAM Required | Description                          |
|--------------------------|--------------|--------------------------------------|
| Reasoner v1              | 8GB          | Advanced reasoning and logic         |
| Llama 3 8B               | 8GB          | Instruction execution specialist     |
| DeepSeek-R1-Distill-Qwen | 8GB          | Deep analysis and insights           |
| Phi-3 Mini Instruct      | 4GB          | Lightweight quick responses          |

---

## Acknowledgments

- Model weights from [HuggingFace](https://huggingface.co)  
- Inspired by [llama-cpp-python](https://github.com/abetlen/llama-cpp-python)  

> **Note**: Models require specific hardware configurations. Phi-3 works on 4GB RAM systems, while others require 8GB+.

---

## License

MIT License  
Copyright (c) 2025 - Silentis Ai

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---
