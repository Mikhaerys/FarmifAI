# FarmifAI (AgroChat Mobile)

![Android](https://img.shields.io/badge/Android-API%2024%2B-3DDC84)
![Mode](https://img.shields.io/badge/Mode-Offline--Only-2E7D32)
![LLM](https://img.shields.io/badge/LLM-Qwen3.5%200.8B%20GGUF-455A64)
![Retrieval](https://img.shields.io/badge/Retrieval-Dense%20Bi--Encoder-1565C0)
![Status](https://img.shields.io/badge/Status-Production%20Prototype-607D8B)

FarmifAI is an Android agricultural assistant focused on robust field operation with local inference.
The master branch is configured as offline-only for inference, using local retrieval + local LLM generation.

## Executive Summary

- Local LLM: Qwen3.5 0.8B GGUF (Q4_K_M) via llama.cpp Android JNI.
- Retrieval pipeline: dense semantic retrieval (bi-encoder style) with cosine similarity ranking.
- Chat UX: explicit reasoning stage support (thinking stream) and final response rendering.
- Vision: plant disease classification pipeline with MindSpore Lite runtime.
- Voice: local STT (Vosk) + local TTS.
- Master policy: online inference path disabled (no Groq inference route in runtime flow).

## Release APK

- Latest release APK (direct):
  - https://raw.githubusercontent.com/Bryan-Andres-Suarez-Sanchez/AgroChat_Project/apk-builds/apk-artifacts/release/latest-release.apk
- Release artifacts folder:
  - https://github.com/Bryan-Andres-Suarez-Sanchez/AgroChat_Project/tree/apk-builds/apk-artifacts/release

## Core Capabilities

1. Agricultural conversational assistant in Spanish.
2. Dense semantic QA over local KB records.
3. Local LLM generation with contextual grounding.
4. Reasoning-aware interaction flow (thinking phase + final answer phase).
5. Image-based disease support for common crops.
6. Voice-first operation for field usage.

## System Architecture

Main assets in this repository:

- System architecture diagram: [docs/assets/fig_system_architecture.png](docs/assets/fig_system_architecture.png)
- RAG pipeline diagram: [docs/assets/fig_rag_pipeline.png](docs/assets/fig_rag_pipeline.png)
- Vision inference diagram: [docs/assets/fig_vision_inference.png](docs/assets/fig_vision_inference.png)

High-level layers:

- UI layer: Compose chat, voice controls, and camera diagnosis flow.
- Orchestration layer: routing, response quality checks, and conversation state.
- Retrieval layer: local embeddings + cosine ranking.
- Generation layer: local llama.cpp runtime (Qwen3.5 GGUF).
- Vision layer: MindSpore Lite disease model.

## Model Stack (Master)

### Local LLM

- Default model: `Qwen3.5-0.8B-Q4_K_M.gguf`
- Runtime: llama.cpp Android JNI bridge
- Download source (runtime): Hugging Face model URL configured in app service

### Semantic Retrieval

- Dense embeddings over local KB
- Bi-encoder style indexing/query encoding
- Cosine similarity ranking for top-k context selection

Scoring equation:

$$
\operatorname{score}(q, d_i) = \frac{q \cdot d_i}{\|q\|\,\|d_i\|}
$$

### Vision Model

- Plant disease classifier for camera-assisted diagnostics
- MindSpore Lite deployment format

## Reasoning Behavior

The chat pipeline supports reasoning-aware rendering:

- If the model emits reasoning tags (`<think>...</think>`), reasoning is handled as a separate thinking phase.
- Final user-facing answer is rendered separately from reasoning text.
- Streaming updates are consolidated into assistant bubbles to keep interaction readable.

## Offline-Only Policy (Master)

Inference behavior in master:

- Online inference route is disabled.
- Response generation uses local LLM only when model is available.
- Retrieval and response orchestration run locally.

Network is still used for one-time model download on first setup.

## Requirements

### Android device

- Android 7.0+ (API 24 or higher)
- Recommended RAM: 4 GB+
- Free storage: depends on downloaded model set

### Development workstation

- Linux/macOS/Windows (WSL supported)
- Android Studio + SDK/NDK
- JDK 11+
- Gradle wrapper included
- Recommended host RAM: 8 GB minimum

## Build

From repository root:

```bash
./gradlew :app:assembleDebug
./gradlew :app:assembleRelease
```

Generated APKs:

- Debug: `app/build/outputs/apk/debug/`
- Release: `app/build/outputs/apk/release/`

## Publish APK Artifact to GitHub (`apk-builds` branch)

```bash
./scripts/build_and_publish_apk.sh release
```

This publishes:

- versioned artifact: `apk-artifacts/release/FarmifAI-release-<timestamp>-<sha>.apk`
- moving link: `apk-artifacts/release/latest-release.apk`

## Repository

- Main repository:
  - https://github.com/Bryan-Andres-Suarez-Sanchez/AgroChat_Project

## Notes

- This project is an engineering prototype for agricultural assistance and decision support.
- Outputs should be validated in real agronomic contexts before high-impact field decisions.