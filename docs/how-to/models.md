---
categories:
- Applied AI
description: Explore available AI models in Dria Network, including Nous, Phi3, and
  Llama variations in various quantized formats.
tags:
- AI models
- Machine Learning
- Dria Network
- Phi3
- Llama
---

# Models

See available models in Dria Network below:

### Available Models

|      Enum      |     Serialized Name     | Description |
| :---: | :---: | :---: |
| `NOUS_THETA` | `finalend/hermes-3-llama-3.1:8b-q8_0` | Nous's Hermes-2-Theta model, q8_0 quantized |
| `PHI3_MEDIUM` | `phi3:14b-medium-4k-instruct-q4_1` | Microsoft's Phi3 Medium model, q4_1 quantized |
| `PHI3_MEDIUM_128K` | `phi3:14b-medium-128k-instruct-q4_1` | Microsoft's Phi3 Medium model, 128k context length, q4_1 quantized |
| `PHI3_5_MINI_OL` | `phi3.5:3.8b` | Microsoft's Phi3.5 Mini model, 3.8b parameters |
| `PHI3_5_MINI_FP16` | `phi3.5:3.8b-mini-instruct-fp16` | Microsoft's Phi3.5 Mini model, 3.8b parameters |
| `GEMMA2_9B_OL` | `gemma2:9b-instruct-q8_0` | Google's Gemma2 model, 9B parameters |
| `GEMMA2_9B_FP16` | `gemma2:9b-instruct-fp16` | Google's Gemma2 model, 9B parameters, fp16 |
| `LLAMA3_1` | `llama3.1:latest` | Meta's Llama3.1 model, 8B parameters |
| `LLAMA3_1_8BQ8` | `llama3.1:8b-instruct-q8_0` | Meta's Llama3.1 model q8 |
| `LLAMA3_1_8B_FP16` | `llama3.1:8b-instruct-fp16` | Meta's Llama3.1 model fp16 |
| `LLAMA3_1_8BTEXTQ4KM` | `llama3.1:8b-text-q4_K_M` | Meta's Llama3.1 model q4 |
| `LLAMA3_1_8BTEXTQ8` | `llama3.1:8b-text-q8_0` | Meta's Llama3.1 model q8 |
| `LLAMA3_1_70B_OL` | `llama3.1:70b-instruct-q4_0` | Meta's Llama3.1 model, 70B parameters |
| `LLAMA3_1_70BQ8` | `llama3.1:70b-instruct-q8_0` | Meta's Llama3.1 model q8 |
| `LLAMA3_1_70BTEXTQ4KM` | `llama3.1:70b-text-q4_0` | Meta's LLama3.1 model fp16 |
| `LLAMA3_2_1B` | `llama3.2:1b` | Meta's LLama3.2 Edge models, 1B parameters |
| `LLAMA3_2_3B` | `llama3.2:3b` | Meta's LLama3.2 Edge models, 3B parameters |
| `LLAMA3_3_70B` | `llama3.3:70b` | Meta's LLama3.3 Edge models, 70B parameters |
| `LLAMA3_2_1BTEXTQ4KM` | `llama3.2:1b-text-q4_K_M` | Meta's LLama3.2 Edge models, 1B parameters, q4 |
| `QWEN2_5_7B_OL` | `qwen2.5:7b-instruct-q5_0` | Alibaba's Qwen2.5 model, 7B parameters |
| `QWEN2_5_7B_FP16` | `qwen2.5:7b-instruct-fp16` | Alibaba's Qwen2.5 model, 7B parameters, fp16 |
| `QWEN2_5_32B_FP16` | `qwen2.5:32b-instruct-fp16` | Alibaba's Qwen2.5 model, 32B parameters, fp16 |
| `QWEN2_5_CODER_1_5B` | `qwen2.5-coder:1.5b` | Alibaba's Qwen2.5 Coder |
| `QWEN2_5_CODER_7B_OL` | `qwen2.5-coder:7b` | AliBaba's Qwen2.5 7b |
| `QWEN2_5_CODER_7B_Q8` | `qwen2.5-coder:7b-instruct-q8_0` | AliBaba's Qwen2.5 7b 8bit |
| `QWEN2_5_CODER_7B_FP16` | `qwen2.5-coder:7b-instruct-fp16` | AliBaba's Qwen2.5 7b 16bit |
| `QWEN_QWQ_OL` | `qwq` | AliBaba's QwenQwq |
| `DEEPSEEK_CODER_6_7B` | `deepseek-coder:6.7b` | DeepSeek Coding models |
| `MIXTRAL_8_7B` | `mixtral:8x7b` | Mistral's MoE Models |
| `DEEPSEEK_R1_1_5B` | `deepseek-r1:1.5b` | R1 Models |
| `DEEPSEEK_R1_7B` | `deepseek-r1:7b` | R1 Models |
| `DEEPSEEK_R1_8B` | `deepseek-r1:8b` | R1 Models |
| `DEEPSEEK_R1_14B` | `deepseek-r1:14b` | R1 Models |
| `DEEPSEEK_R1_32B` | `deepseek-r1:32b` | R1 Models |
| `DEEPSEEK_R1_70B` | `deepseek-r1:70b` | R1 Models |
| `GPT4_TURBO` | `gpt-4-turbo` | OpenAI's GPT-4 Turbo model |
| `GPT4O` | `gpt-4o` | OpenAI's GPT-4o model |
| `GPT4O_MINI` | `gpt-4o-mini` | OpenAI's GPT-4o mini model |
| `O1_MINI` | `o1-mini` | OpenAI's o1 mini model |
| `O1_PREVIEW` | `o1-preview` | OpenAI's o1 preview model |
| `O1` | `o1` | OpenAI's o1 model |
| `GEMINI_20_FLASH` | `gemini-2.0-flash-exp` | Gemini 2.0 Flash exp model |
| `GEMINI_15_PRO` | `gemini-1.5-pro` | Gemini 1.5 Pro model |
| `GEMINI_15_FLASH` | `gemini-1.5-flash` | Gemini 1.5 Flash model |
| `GEMINI_10_PRO` | `gemini-1.0-pro` | Gemini 1.0 Pro model |
| `GEMMA_2_2B_IT` | `gemma-2-2b-it` | Gemma 2 2B IT model |
| `GEMMA_2_9B_IT` | `gemma-2-9b-it` | Gemma 2 9B IT model |
| `GEMMA_2_27B_IT` | `gemma-2-27b-it` | Gemma 2 27B IT model |
| `LLAMA_3_1_8B_OR` | `meta-llama/llama-3.1-8b-instruct` | OpenRouter Models |
| `LLAMA_3_1_70B_OR` | `meta-llama/llama-3.1-70b-instruct` | OpenRouter Models |
| `LLAMA_3_1_405B_OR` | `meta-llama/llama-3.1-405b-instruct` | OpenRouter Models |
| `LLAMA_3_1_70B_OR_F` | `meta-llama/llama-3.1-70b-instruct:free` | OpenRouter Models |
| `LLAMA_3_3_70B_OR` | `meta-llama/llama-3.3-70b-instruct` | OpenRouter Models |
| `ANTHROPIC_SONNET_3_5_OR` | `anthropic/claude-3.5-sonnet:beta` | OpenRouter Models |
| `ANTHROPIC_HAIKU_3_5_OR` | `anthropic/claude-3-5-haiku-20241022:beta` | OpenRouter Models |
| `QWEN2_5_72B_OR` | `qwen/qwen-2.5-72b-instruct` | OpenRouter Models |
| `QWEN2_5_7B_OR` | `qwen/qwen-2.5-7b-instruct` | OpenRouter Models |
| `QWEN2_5_CODER_32B_OR` | `qwen/qwen-2.5-coder-32b-instruct` | OpenRouter Models |
| `QWEN2_5_EVA_32B_OR` | `eva-unit-01/eva-qwen-2.5-32b` | OpenRouter Models |
| `QWEN_QWQ_OR` | `qwen/qwq-32b-preview` | OpenRouter Models |
| `DEEPSEEK_2_5_OR` | `deepseek/deepseek-chat` | OpenRouter Models |
| `NOUS_HERMES_405B_OR` | `nousresearch/hermes-3-llama-3.1-405b` | OpenRouter Models |