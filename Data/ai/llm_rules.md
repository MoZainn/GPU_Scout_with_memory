# Local LLM Deployment Guide

This document explains how GPU specifications affect running local Large Language Models (LLMs).

---

# What determines whether a GPU can run an LLM?

The most important factor is VRAM.

If the model cannot fit inside GPU VRAM, inference becomes slower because part of the model must be stored in system RAM.

---

# VRAM Requirements

Approximate VRAM requirements.

## Llama 3 8B

FP16:
16 GB

Q8:
10–12 GB

Q6:
8–10 GB

Q4:
5–6 GB

---

## Llama 3 70B

FP16:
140 GB

Q8:
70 GB

Q6:
55 GB

Q4:
35–45 GB

---

## DeepSeek R1 7B

Q4:
5–6 GB

---

## DeepSeek R1 70B

Q4:
40–50 GB

---

## Mistral 7B

Q4:
5 GB

---

## Mixtral 8x7B

Q4:
26–32 GB

---

# General Rules

More VRAM allows:

- Larger models
- Larger context windows
- Faster inference
- Larger batch sizes

---

If VRAM is insufficient:

The model may use CPU offloading.

CPU offloading reduces speed significantly.

---

Quantization reduces memory usage.

Lower-bit quantization slightly reduces model quality but greatly lowers VRAM requirements.

---

Tensor Cores accelerate inference.

Memory bandwidth improves token generation speed.

---

CUDA provides the best compatibility for AI software.

Most AI frameworks are optimized for NVIDIA GPUs.

---

ROCm allows many AMD GPUs to run LLMs, although software compatibility is generally lower than CUDA.

---

# Recommendation Rules

For beginners:

8–12 GB VRAM is sufficient for 7B models.

For enthusiasts:

16–24 GB VRAM is ideal.

For AI developers:

24 GB or more is strongly recommended.

For 70B models:

Use

- multiple GPUs,

or

- enterprise GPUs,

or

- aggressive quantization with CPU offloading.