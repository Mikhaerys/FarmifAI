Qué debe lograr tu README
Tu README debe responder tres cosas, en este orden:
�. Qué problema resuelve
�. Por qué tu solución es técnicamente sólida
�. Cómo la prueba un jurado en menos de 5 minutos
Para tu caso —una app móvil Android con un LLM offline para agricultura
— el README tiene que vender a la vez impacto, ingeniería y
verificabilidad. Esa combinación encaja muy bien con lo que GitHub
recomienda documentar en un README, con lo que Android considera
importante para apps robustas/offline-first, y con la estructura de
documentación de modelos que Hugging Face usa para dejar claro uso,
limitaciones, datos y evaluación.
Estructura ganadora para tu README
1) Encabezado “hero” arriba de todo
Pon, sin rodeos:
• Nombre del proyecto
• One-liner potente
• Badges mínimos
• Imagen principal o mockup
• Enlaces visibles a demo, APK y video
GitHub recomienda que el README sea la puerta de entrada del repositorio,
y además permite mostrar workflow badges directamente en el README.
También puedes definir una social preview image para que el repo luzca
bien cuando lo compartas.
Ejemplo de one-liner:
GitHub Docs +4
GitHub Docs +2
AgroChat Mobile is an Android offline-first assistant that uses a local
LLM to answer agricultural questions in Spanish without requiring
Ese subtítulo debe dejar clarísimo:
• plataforma: Android
• valor técnico: local LLM
• valor social: agricultura
• diferenciador: offline
2) Demo primero, no escondida
Después del hero, la siguiente sección debe ser Demo:
• video de 1–3 minutos
• screenshots
• APK o instrucciones de instalación
• credenciales de prueba, si existen
• pasos exactos de validación
Esto es clave para competición: Devpost suele pedir video y materiales
visuales, y hay reglas donde se aclara que los jueces podrían basarse sólo en
el material presentado.
Haz una subsección llamada Quick evaluation path con algo así:
�. Descargar el APK
�. Instalar en Android
�. Abrir la app
�. Probar tres prompts sugeridos
�. Verificar que responde sin internet
Eso reduce fricción y sube mucho la evaluabilidad.
3) Problema y contexto
Luego explica:
• problema real del agricultor
• por qué la conectividad limitada importa
internet connectivity.
help.devpost.com +2
• por qué un enfoque offline es relevante
• a quién va dirigida la app
Aquí no te extiendas demasiado. Dos o tres párrafos bastan. La idea es que
el jurado entienda el caso de uso antes de entrar al código.
4) Solución y propuesta de valor
Incluye una sección What this app does o Key features con 5–7 puntos
máximos. Ejemplo:
• consultas agronómicas en español
• inferencia local sin internet
• recuperación de conocimiento local
• respuesta optimizada para gama media
• historial o persistencia local
• modo de uso para campo
GitHub recomienda que el README deje claro qué hace el proyecto y por
qué es útil.
5) Arquitectura técnica
Esta sección debe ser una de las más fuertes en tu caso.
Android recomienda separar responsabilidades con una arquitectura en
capas y, como mínimo, distinguir UI layer y Data layer, con una Domain
layer opcional. También enfatiza separation of concerns. Para una app
offline-first, Android recomienda que haya una fuente local y que la app
pueda seguir funcionando sin red; además, el origen local debe ser la fuente
canónica de verdad para lo que leen las capas superiores.
Para tu README, eso se traduce en un diagrama y una explicación breve
como esta:
• UI layer: pantallas de chat, resultados, historial
• Domain layer: orquestación del flujo consulta → recuperación →
inferencia → respuesta
GitHub Docs
Android Developers +1
• Data layer: base local, embeddings, recursos agrícolas, modelo local
• Inference engine: runtime del LLM local
• Optional fallback: si existe modo online, marcarlo claramente como
opcional
Pon un diagrama sencillo en docs/architecture.png y embébelo en el
README con ruta relativa. GitHub recomienda usar relative links e image
paths dentro del repositorio.
6) Sección específica del modelo
Aquí debes tratar el LLM como un componente serio, no como una caja
negra.
Hugging Face recomienda que la documentación del modelo incluya al
menos:
• descripción del modelo
• usos previstos y limitaciones
• datasets usados
• parámetros o detalles del entrenamiento
• resultados de evaluación
Entonces en tu README crea una sección Model & AI pipeline con estos
subtítulos:
• Base model
• Quantization / format
• On-device runtime
• Knowledge source
• Intended use
• Out-of-scope use
• Known limitations
• Evaluation results
En tu caso conviene especificar cosas como:
• nombre del modelo base
GitHub Docs +1
Hugging Face +1
• tamaño del archivo
• formato del modelo
• idioma principal
• si hubo fine-tuning o sólo RAG
• si las respuestas son generativas, extractivas o híbridas
• qué no debe usarse para decidir
• qué tareas sí resuelve bien
7) Evaluación y métricas
No pongas “funciona bien”. Pon evidencia.
La parte de evaluación del modelo debe incluir:
• conjunto de pruebas
• número de preguntas o escenarios
• métricas
• resultados
• limitaciones del benchmark
Para una app móvil con LLM offline, las métricas más valiosas en README
son:
• tiempo medio de respuesta
• tamaño del modelo
• uso de RAM aproximado
• tiempo de arranque
• precisión o tasa de acierto en preguntas agrícolas
• funcionamiento sin red
• dispositivo de prueba
Android trata el rendimiento, incluido el startup time, como un aspecto
importante de calidad de app.
Lo ideal es una subsección Benchmarks on device con resultados reales,
por ejemplo:
Hugging Face +2
Android Developers +1
• Device: Redmi 12 / 8 GB RAM
• Android version: 14
• Model size: 1.2 GB
• Avg first token latency: X ms
• Avg full response latency: Y s
• Offline success rate: Z%
• Domain QA accuracy: N/M
8) Privacidad, seguridad y permisos
Esta parte da muchísima seriedad en una competición.
Android recomienda pedir sólo el mínimo número de permisos necesarios y
documentar claramente por qué se usan.
Entonces incluye una sección Privacy, Security & Permissions:
• qué datos se procesan localmente
• qué datos no salen del dispositivo
• si se requiere internet o no
• qué permisos usa la app y por qué
• si el micrófono, almacenamiento o cámara son opcionales
• si existe telemetría, analítica o no
Ejemplo de redacción:
Eso les dice a los jueces que no estás ocultando cosas.
9) Instalación y ejecución
Aquí debes pensar en alguien que no conoce tu stack.
GitHub dice que el README debe explicar cómo empezar con el proyecto.
Android Developers +1
All core inference runs locally on-device. The app does not require
continuous internet access for its main workflow. It only requests the
minimum permissions required for its enabled features.
Divide esta sección así:
• For judges
APK + pasos mínimos
• For developers
clonado, requisitos, build, assets del modelo, variables, ejecución
• For reproducibility
qué archivos no vienen en el repo y cómo obtenerlos
Muy importante para tu caso: GitHub bloquea archivos mayores a 100 MiB,
y para más de ese límite debes usar Git LFS. Además, si necesitas distribuir
binarios grandes, GitHub sugiere considerar releases.
Como tu proyecto usa modelo local, el README debe dejar explícito si:
• el modelo está en Git LFS
• el modelo se descarga desde Releases
• el modelo se obtiene desde un enlace externo
• no se incluye por licencia o tamaño
No dejes eso implícito.
10) Estructura del repositorio
Pon un árbol corto, no gigante. Ejemplo:
GitHub Docs
GitHub Docs +1
app/ # Android app
docs/ # diagrams, screenshots, extra technical notes
models/ # model loader or references (not necessarily wei
data/ # local KB or examples
scripts/ # helper scripts
README.md
LICENSE
CITATION.cff
SECURITY.md
GitHub recomienda complementar el README con archivos como LICENSE,
CITATION, CONTRIBUTING y otros documentos que clarifican expectativas
del proyecto.
11) Limitaciones y trabajo futuro
Esta sección sube credibilidad.
Inspirado en la estructura de model cards, debes incluir:
• límites del modelo
• tipos de error conocidos
• casos fuera de alcance
• mejoras planeadas
Ejemplos:
• no sustituye asesoría agronómica profesional
• rendimiento variable en consultas ambiguas
• cobertura limitada a ciertos cultivos o regiones
• respuestas dependientes de la base de conocimiento local
• aún no optimizado para todos los dispositivos Android
Un README que admite límites suele verse más serio que uno que promete
demasiado.
Archivos extra que elevan mucho el nivel
Además de README.md , yo pondría:
• LICENSE
• CITATION.cff
• SECURITY.md
• CONTRIBUTING.md (aunque sea corto)
• docs/architecture.md
• docs/evaluation.md
GitHub documenta específicamente el valor de CITATION.cff ,
GitHub Docs +4
Hugging Face +1
SECURITY.md y CONTRIBUTING.md para hacer el proyecto más claro y
mantenible.
Reglas de estilo para que el README se vea profesional
�. Pon lo importante arriba.
El jurado no debe hacer scroll para entender el proyecto.
�. Usa encabezados claros.
GitHub genera automáticamente un outline/tabla de contenido a partir
de los headings, así que conviene una jerarquía limpia con ## y ### .
�. Usa rutas relativas para imágenes y docs.
Así los enlaces siguen funcionando al cambiar de rama o al clonar el
repo.
�. No hagas un README monstruoso.
GitHub trunca contenido más allá de 500 KiB; conviene dejar el
README como puerta de entrada y mover anexos a docs/ .
�. Incluye imágenes reales del producto.
Mockups, screenshots y diagrama técnico valen más que párrafos
largos. Devpost además suele pedir galería visual.
�. No entierres el video demo.
Déjalo arriba o en el primer tercio del README. En muchas
competencias el demo pesa mucho en la evaluación.
Orden exacto que te recomiendo
Éste sería mi orden ideal para tu caso:
GitHub Docs +3
GitHub Docs +1
GitHub Docs +1
GitHub Docs
help.devpost.com +1
help.devpost.com +1
Markdown
Plantilla mínima de alto nivel
# Project title
Badges
One-line pitch
Hero image / screenshot
## Demo
## Quick evaluation path
## Problem
## Solution
## Key features
## System architecture
## AI / Model details
## Offline-first design
## Evaluation and benchmarks
## Privacy, security and permissions
## Installation
## Build from source
## Repository structure
## Limitations
## Future work
## License
## Citation
## Acknowledgements
Markdown
# AgroChat Mobile
[badges]
> Offline-first Android assistant for agriculture powered by a local L
![Hero image](docs/images/hero.png)
## Demo
- Video:
- APK:
- Slides:
- Quick test steps:
## Quick evaluation path
1. Install APK
2. Disable internet
3. Ask one of the sample agricultural questions
4. Verify local response
5. Review architecture and benchmarks below
## Problem
...
## Solution
...
## Key features
- ...
- ...
- ...
## System architecture
![Architecture](docs/images/architecture.png)
## AI / Model details
### Base model
### Runtime
### Knowledge base
### Intended use
### Out-of-scope use
### Known limitations
## Offline-first design
## Offline-first design
...
## Evaluation and benchmarks
| Metric | Value |
|---|---|
| Device | ... |
| Avg latency | ... |
| Model size | ... |
| Offline success rate | ... |
## Privacy, security and permissions
...
## Installation
...
## Build from source
...
## Repository structure
```text
...
Limitations
...
Future work
...
License
See LICENSE
Citation
See CITATION.cff
Security
See SECURITY.md
## Qué suele bajar el nivel de un README en competencias
- explicar demasiado el problema y muy poco la solución
- no mostrar screenshots reales
- no incluir ruta de prueba rápida
- esconder el APK o demo
- no aclarar cómo se obtiene el modelo
- decir “offline” sin demostrarlo
- no incluir limitaciones
- pedir permisos sin justificarlos
- no mostrar métricas en dispositivo real
## Mi recomendación final
Para tu app, el README ideal no debe parecer sólo un documento de GitH
- **landing page para jurados**
- **nota técnica de arquitectura Android**
- **mini model card**
- **manual de validación rápida**
Esa combinación está muy alineada con lo que recomiendan GitHub, Andro
Compárteme el nombre de la app, stack exacto, modelo local y métricas
::contentReference[oaicite:22]{index=22}