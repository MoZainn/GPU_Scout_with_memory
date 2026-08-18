# Gaming Performance Guide

This document covers general rules for how GPU specs translate into
gaming performance, independent of any single GPU model.

---

## Resolution and VRAM

1080p: 8 GB VRAM is generally sufficient for current titles.
1440p: 10-12 GB VRAM is recommended for high texture settings.
4K: 16 GB+ VRAM is recommended, especially with ray tracing enabled.

---

## Frame Rate Targets

Competitive gaming (Valorant, CS2, Fortnite):
Target 144+ FPS. CPU and low-latency rendering matter more than
raw GPU power once a GPU can already hit high frame rates.

Single-player / cinematic games (Cyberpunk 2077, story-driven AAA):
Target 60-120 FPS. GPU power, ray tracing performance, and upscaling
quality matter more here than pure CPU speed.

---

## Upscaling Technologies

DLSS (NVIDIA): AI upscaling, generally the highest quality of the
major upscalers, requires an NVIDIA GPU with Tensor Cores.

FSR (AMD): Works across NVIDIA, AMD, and Intel GPUs, quality has
improved significantly in recent versions but historically trails DLSS.

Frame Generation: Interpolates extra frames using AI. Increases
displayed FPS but does not reduce input latency the way real
rendered frames do — best for already-high base frame rates.

---

## Ray Tracing

Ray tracing performance depends heavily on dedicated RT cores.
Full path tracing (e.g. Cyberpunk 2077 Overdrive mode) is extremely
demanding and generally requires a flagship-tier GPU plus upscaling
to run at playable frame rates.

---

## CPU Bottlenecks in Gaming

At 1080p, CPU bottlenecks are common even with mid-range GPUs,
since the GPU can render frames faster than the CPU can prepare them.

At 4K, the GPU becomes the primary bottleneck for almost all
current CPUs, so upgrading the GPU has more impact than the CPU.

---

## Practical Recommendations

For competitive esports titles: prioritize a fast CPU and a GPU
that comfortably exceeds your monitor's refresh rate.

For AAA single-player titles at high settings: prioritize GPU VRAM,
ray tracing performance, and upscaling support.

For 4K gaming: prioritize VRAM (16GB+), memory bandwidth, and a
GPU with strong native 4K performance rather than relying on
upscaling alone.
