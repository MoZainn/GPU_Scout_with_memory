# Local LLM VRAM Requirements

Llama 7B:
- FP16: approximately 14 GB VRAM
- Q4 quantized: approximately 4-6 GB VRAM

Llama 13B:
- FP16: approximately 26 GB VRAM
- Q4 quantized: approximately 8-10 GB VRAM

Llama 34B:
- FP16: approximately 68 GB VRAM
- Q4 quantized: approximately 18-24 GB VRAM

Llama 70B:
- FP16: approximately 140 GB VRAM
- Q4 quantized: approximately 35-45 GB VRAM

DeepSeek R1 70B:
- Requires approximately 40-50 GB VRAM when quantized.

RTX 4090:
- Contains 24 GB GDDR6X VRAM.

An RTX 4090 can run:
- Llama 7B
- Llama 13B
- Llama 34B quantized
- Some 70B models with aggressive quantization and offloading

An RTX 4090 cannot comfortably run:
- Full precision 70B models.