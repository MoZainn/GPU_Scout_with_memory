# PC Hardware Guide

This document covers general hardware considerations around
running a GPU: power, cooling, and compatibility.

---

## PSU (Power Supply) Sizing

Rule of thumb: take the GPU's rated TDP, add the rest of the
system (CPU, drives, fans, motherboard) — roughly 150-250W for a
typical build — and add 20% headroom for transient power spikes
and PSU efficiency losses.

Example: a 450W GPU + ~200W rest-of-system = 650W total load.
Recommended PSU: 750-850W to leave headroom.

High-end GPUs (500W+) often specify their own minimum PSU wattage
directly — always follow the manufacturer's stated recommendation
over a generic rule of thumb.

Look for an 80 Plus Gold (or better) rated PSU for efficiency,
and make sure it has the correct PCIe power connectors for the GPU
(some newer flagship GPUs use a single 12VHPWR connector).

---

## Cooling and Airflow

GPUs generate significant heat under load. Case airflow matters
as much as the GPU's own cooler:

- Front intake fans + rear/top exhaust fans create a clear airflow path.
- Poor airflow can cause thermal throttling even on a well-cooled GPU.
- Ambient room temperature affects sustained performance, especially
  for multi-hour AI training or rendering jobs.

Thermal throttling reduces clock speeds automatically once the GPU
hits its temperature limit, which lowers performance even though
the GPU itself is technically fine.

---

## CPU Bottlenecks

A CPU bottleneck happens when the CPU cannot feed the GPU work fast
enough, so the GPU sits partially idle waiting for instructions.

More common at:
- Lower resolutions (1080p)
- High refresh rate competitive gaming
- Older or budget CPUs paired with a high-end GPU

Less common at:
- 4K gaming (GPU-bound almost always)
- AI/ML workloads (GPU-bound, CPU mostly just orchestrates)

---

## PCIe and Motherboard Compatibility

PCIe generation (3.0 / 4.0 / 5.0) has a small impact on gaming
performance for most current GPUs, since few GPUs saturate even
PCIe 4.0 x16 bandwidth in real workloads.

Physical slot compatibility matters more: PCIe x16 slots are
backward and forward compatible, but running a PCIe 5.0 GPU in a
PCIe 3.0 slot will cap it at PCIe 3.0 bandwidth, which can slightly
affect performance for AI workloads that move large amounts of data.

Always check case clearance (GPU length/height/thickness) before
buying — flagship GPUs are often physically large (3-4 slots wide).

---

## Power Consumption Summary

Higher-end GPUs consume significantly more power and produce more
heat. Before upgrading a GPU, always verify:

1. Your PSU wattage and connector types.
2. Your case's airflow and physical clearance.
3. Your CPU won't badly bottleneck the new GPU at your target resolution.
