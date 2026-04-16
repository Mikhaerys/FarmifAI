# FarmifAI

FarmifAI es una aplicacion Android para asistencia agricola en campo. El proyecto integra consulta conversacional, recuperacion aumentada por conocimiento local, razonamiento con un modelo generativo GGUF y diagnostico visual de enfermedades vegetales con inferencia en dispositivo.

La documentacion tecnica consolidada del proyecto se mantiene en un unico informe:

[docs/FarmifAI_Informe_Avances.docx](docs/FarmifAI_Informe_Avances.docx)

## Estado Del Proyecto

- Rama principal: `master`.
- Modo de ejecucion: local en dispositivo, sin servicios remotos en el flujo de aplicacion.
- Modelo generativo objetivo: Qwen 3.5 en formato GGUF cuantizado.
- Runtime LLM: `llama.cpp` mediante JNI Android.
- Recuperacion de conocimiento: KB local con embeddings de 384 dimensiones y fallback lexical local.
- Vision: clasificador MindSpore Lite para enfermedades de plantas.
- Feedback: registro local JSONL en el almacenamiento privado de la app.

## Capacidades Principales

- Chat agricola en espanol con contexto local.
- RAG sobre una base de conocimiento empaquetada en `app/src/main/assets/kb_nueva/extract`.
- Separacion de razonamiento y respuesta final para modelos que emiten trazas tipo `<think>`.
- Enrutamiento de respuesta con politica explicita: `KB_DIRECT`, `LLM_WITH_KB`, `LLM_GENERAL` y `ABSTAIN`.
- Diagnostico visual con 21 clases distribuidas en cafe, maiz, papa, pimiento y tomate.
- Entrada por voz con Vosk cuando el modelo de voz esta provisionado localmente.
- Sintesis de voz mediante el motor TTS del sistema.

## Evidencia Local Versionada

El informe de avances resume y contextualiza la evidencia real del repositorio. Como referencia rapida:

| Componente | Evidencia |
|---|---|
| Base de conocimiento | 12 archivos JSONL, 293 registros agronomicos |
| Embeddings | `kb_embeddings.npy`, matriz `(2842, 384)` en `float32` |
| Mapeo RAG | `kb_embeddings_mapping.json` |
| LLM local | `LlamaService.kt` usa `Qwen3.5-0.8B-Q4_K_M.gguf` como modelo preferido |
| Razonamiento | `MainActivity.kt` separa contenido `<think>` y respuesta visible |
| Vision | `plant_disease_labels.json` declara 21 clases y `plant_disease_model_old.ms` se carga desde assets |
| Feedback | `FeedbackEventStore.kt` persiste eventos localmente en JSONL |

## Arquitectura

FarmifAI se organiza en cuatro capas funcionales:

1. Interfaz Android: Jetpack Compose para chat, voz, configuracion y diagnostico visual.
2. Orquestacion: `MainActivity.kt` coordina estado, enrutamiento, streaming local, diagnostico y feedback.
3. Inteligencia local: `SemanticSearchHelper.kt`, `LlamaService.kt`, `PlantDiseaseClassifier.kt` y puentes JNI.
4. Datos locales: registros JSONL, embeddings, mapeos, etiquetas de vision y modelos provisionados.

La rama `master` no declara permisos de red, no incluye clientes HTTP para LLM remoto y no sincroniza feedback hacia endpoints externos.

## Requisitos

- Android Studio reciente.
- JDK 11.
- Android SDK y NDK configurados.
- Dispositivo o emulador Android API 24+.
- Modelo GGUF local compatible con Qwen 3.5 para habilitar generacion en dispositivo.

## Compilacion

Compilar APK debug:

```bash
./gradlew :app:assembleDebug
```

Ejecutar pruebas unitarias:

```bash
./gradlew :app:testDebugUnitTest
```

Tambien se conserva el script auxiliar de construccion:

```bash
./scripts/build_apk.sh debug
```

## Provisionamiento Local De Modelos

El repositorio mantiene los datos y modelos livianos necesarios para documentar y validar la arquitectura. Los modelos pesados se tratan como artefactos locales.

- Copiar el GGUF preferido a la carpeta externa privada de la aplicacion. El nombre recomendado es `Qwen3.5-0.8B-Q4_K_M.gguf`.
- Para el encoder semantico opcional, provisionar `sentence_encoder.ms` y `sentence_tokenizer.json` en `files/models`.
- Si el encoder no esta disponible, la app conserva recuperacion local mediante fallback lexical.
- Para voz STT con Vosk, provisionar el directorio `model-es-small` localmente o incluirlo como asset.

## Estructura Del Repositorio

```text
AgroChat_Project/
  app/           # Aplicacion Android, assets locales y codigo de inferencia
  docs/          # Informe unico de avances del proyecto
  nlp_dev/       # Herramientas de procesamiento y experimentacion NLP
  tools/         # Entrenamiento/exportacion de vision
  scripts/       # Scripts de build, instalacion y despliegue local
  pc_rag_clone/  # Replica de experimentacion y vendor llama.cpp
  README.md
```

## Alcance Y Limitaciones

FarmifAI esta orientado a asistencia tecnica preliminar y educativa. No sustituye el criterio de un agronomo certificado en decisiones de alto riesgo. La cobertura de respuestas depende de la KB local y de los modelos provisionados en el dispositivo. El informe de avances documenta las evidencias verificables y evita declarar metricas no respaldadas por archivos versionados.

## Referencia Tecnica

Para detalles de arquitectura, evidencia, decisiones de diseno y estado de avance, consultar exclusivamente:

[docs/FarmifAI_Informe_Avances.docx](docs/FarmifAI_Informe_Avances.docx)
