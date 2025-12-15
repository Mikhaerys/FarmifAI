
# AgroChat (ARApp)

Asistente agrícola para Android con IA offline: STT (Vosk), búsqueda semántica (MindSpore Lite), RAG y LLM local (llama.cpp). Opcionalmente permite LLM online (Groq).

## Requisitos

- Android Studio + JDK 17
- NDK 25.1.8937393 y CMake 3.22.1
- `adb` (Android platform-tools)
- Git LFS (el repo usa LFS para assets grandes)
- Dispositivo Android arm64-v8a (recomendado) con USB debugging

## Clonar y preparar (nuevo en el proyecto)

```bash
git clone https://github.com/Bryan-Andres-Suarez-Sanchez/AgroChat_Project.git
cd AgroChat_Project

git lfs install
git lfs pull
```

Si estás trabajando en esta versión (diagnóstico visual + Llama autodetect):

```bash
git checkout feature/diagnostico-visual
```

## Compilar e instalar

```bash
./gradlew :app:assembleDebug
./gradlew :app:installDebug
adb shell am start -n edu.unicauca.app.agrochat/.MainActivity
```

Logs útiles:

```bash
adb logcat -s MainActivity LlamaService LLamaAndroid SemanticSearchHelper PlantDiseaseClassifier
```

## Modelos/Assets usados por la app

Todo lo que la app necesita en runtime está bajo `app/src/main/assets/` (y se versiona con Git LFS cuando aplica), excepto el modelo GGUF de Llama.

- Búsqueda semántica (MindSpore):
  - `sentence_encoder.ms` (embeddings)
  - `sentence_tokenizer.json`
  - `kb_embeddings.npy` + `agrochat_knowledge_base.json`
- Voz (Vosk STT): `model-es-small/`
- Diagnóstico visual (MindSpore):
  - `plant_disease_model.ms`
  - `plant_disease_labels.json`

## Llama offline funcionando en el celular (GGUF)

Por diseño, el modelo `.gguf` NO se guarda en el repositorio. La app lo carga desde el almacenamiento de la app en el teléfono:

`/sdcard/Android/data/edu.unicauca.app.agrochat/files/`

1) Consigue un modelo GGUF compatible (ej. Llama 3.x Instruct cuantizado).

2) Cópialo al teléfono:

```bash
tools/push_llama_model_to_device.sh /ruta/al/modelo.gguf
```

3) Reinicia la app y verifica logs:

```bash
adb shell am force-stop edu.unicauca.app.agrochat
adb shell am start -n edu.unicauca.app.agrochat/.MainActivity
adb logcat -s MainActivity LlamaService LLamaAndroid
```

Debes ver algo como “Modelo cargado exitosamente”.

## Diagnóstico visual (modelo Colombia)

El diagnóstico usa MindSpore Lite con `plant_disease_model.ms` + `plant_disease_labels.json` (21 clases, incluye Café).

Para debug:

```bash
adb logcat -s PlantDiseaseClassifier
```

## Actualizar la base de conocimiento (KB) y embeddings

1) Edita `app/src/main/assets/agrochat_knowledge_base.json`.

2) Regenera embeddings (requiere Python 3.10+):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install numpy torch transformers sentence-transformers

python generate_mindspore_compatible_embeddings.py
python generate_embeddings.py
```

3) Recompila e instala.

Nota: el runtime valida la compatibilidad tokenizer/embeddings en logs cuando MindSpore está activo.

## LLM online (Groq) (opcional)

La app soporta modo online si configuras la API key dentro de la app (Settings).

## Estructura (lo esencial)

```
app/src/main/java/edu/unicauca/app/agrochat/
  MainActivity.kt
  llm/LlamaService.kt
  mindspore/SemanticSearchHelper.kt
  vision/PlantDiseaseClassifier.kt

app/src/main/assets/
  sentence_encoder.ms
  sentence_tokenizer.json
  kb_embeddings.npy
  agrochat_knowledge_base.json
  plant_disease_model.ms
  plant_disease_labels.json
  model-es-small/
```
