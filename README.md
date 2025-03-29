# Silentis AI - Open Source Python Plugin  
**MIT License | Version 1.0**  

A flexible AI plugin system for interacting with multiple large language models, featuring:  
✅ **Multi-model support** (Reasoner, Llama, DeepSeek, Phi-3)  
✅ **GPU acceleration** toggle  
✅ **Customizable parameters** (temperature, max tokens, Top-P)  
✅ **RAM requirement checks**  
✅ **Persistent configuration**  
✅ **Interactive chat interface**  

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

## Installation  
1. Clone repository:  
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

## Usage  
1. Run the plugin:  
   ```bash
   python run.py
   ```

2. Follow on-screen instructions:  
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
   - Type `quit` to return to menu  
   - Model shows "Thinking..." while generating responses  

## Configuration  
Modify `config.json` or use in-app settings (option 10):  
```json
{
  "system_prompt": "You are Silentis...",
  "model_params": {
    "temp": 0.7,
    "max_tokens": 50,
    "top_p": 0.9
  },
  "use_gpu": false
}
```

## License  
[MIT License](LICENSE) - Copyright (c) 2025 [Silentis]  

## Acknowledgments  
- Model weights from [HuggingFace](https://huggingface.co)  
- Inspired by [llama-cpp-python](https://github.com/abetlen/llama-cpp-python)  

> **Note**: Models require specific hardware configurations. Phi-3 works on 4GB RAM systems, while others require 8GB+. [[1]][[5]][[7]]  
