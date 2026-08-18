# GPU Comparison Rules

These rules help compare GPUs for AI, gaming, rendering, and professional workloads.

---

## VRAM

Higher VRAM allows larger datasets, textures, and AI models to fit entirely in GPU memory.

If a model exceeds available VRAM:

- Quantization may help.
- CPU offloading may be required.
- Performance usually decreases.

More VRAM is usually better for:

- Local LLMs
- Stable Diffusion
- Video editing
- 3D rendering
- Large gaming texture packs

---

## CUDA Cores

CUDA Cores perform general GPU computations.

Higher CUDA Core counts generally improve:

- AI inference
- Rendering
- Physics simulations
- Gaming performance

CUDA Core count alone does not determine overall performance.

Architecture also matters.

---

## Tensor Cores

Tensor Cores accelerate matrix multiplication.

Tensor Cores improve:

- LLM inference
- AI training
- Stable Diffusion
- DLSS
- Deep Learning

More Tensor Cores generally improve AI workloads.

---

## RT Cores

RT Cores accelerate ray tracing.

Higher RT Core performance improves:

- Ray tracing
- Path tracing
- Lighting realism

---

## Memory Bandwidth

Higher bandwidth allows faster movement of data.

Higher bandwidth benefits:

- Large LLMs
- Stable Diffusion
- Scientific computing
- 4K gaming

Bandwidth becomes increasingly important as VRAM usage grows.

---

## Architecture

Newer architectures usually improve:

- Performance per watt
- AI acceleration
- Ray tracing
- Memory efficiency

Architecture improvements often outperform raw core count increases.

---

## PCIe

PCIe version has relatively small impact on gaming.

AI workloads benefit more from VRAM than PCIe generation.

---

## Power Consumption

Higher-end GPUs generally consume more power.

Always verify PSU recommendations before upgrading.

---

## Consumer vs Professional GPUs

Consumer GPUs are excellent for:

- Gaming
- Local AI
- Stable Diffusion
- Content creation

Professional GPUs are better suited for:

- Large AI training
- Enterprise deployment
- ECC memory
- Multi-GPU servers

---

## GPU Selection Rules

If the workload is AI:

Prioritize:

1. VRAM
2. Tensor Cores
3. Memory Bandwidth

If the workload is gaming:

Prioritize:

1. GPU Architecture
2. RT Cores
3. Memory Bandwidth

If the workload is rendering:

Prioritize:

1. VRAM
2. CUDA Cores
3. Memory Bandwidth

If two GPUs have similar specifications:

Prefer the newer architecture.