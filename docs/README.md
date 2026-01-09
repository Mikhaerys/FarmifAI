# FarmifAI Documentation

This directory contains the technical documentation and academic papers for the FarmifAI project.

## Contents

### Diagrams (Auto-generated)

| File | Description |
|------|-------------|
| `fig_system_architecture.png` | On-device system architecture |
| `fig_training_architecture.png` | Training pipeline for Vision & NLP models |
| `fig_rag_pipeline.png` | RAG (Retrieval-Augmented Generation) pipeline |
| `fig_vision_inference.png` | Vision model inference pipeline |
| `fig_two_phase_training.png` | Two-phase transfer learning strategy |
| `fig_deployment_workflow.png` | Model deployment workflow |

### LaTeX Papers

| File | Language | Description |
|------|----------|-------------|
| `FarmifAI_Paper_EN.tex` | English | Complete technical paper |
| `FarmifAI_Paper_ES.tex` | Spanish | Complete technical paper |

## Generating Diagrams

The diagrams are generated using Python and matplotlib:

```bash
cd /path/to/AgroChat_Project
source .venv/bin/activate
pip install matplotlib numpy
python docs/generate_diagrams.py
```

## Compiling PDFs

### Prerequisites

Install LaTeX on your system:

**Ubuntu/Debian:**
```bash
sudo apt-get install texlive-latex-base texlive-latex-extra \
    texlive-fonts-recommended texlive-lang-spanish
```

**Fedora:**
```bash
sudo dnf install texlive-scheme-medium texlive-babel-spanish
```

**macOS:**
```bash
brew install --cask mactex-no-gui
```

**Windows:**
- Download and install [MiKTeX](https://miktex.org/download)

### Compilation

Use the provided script:

```bash
cd docs/
chmod +x compile_papers.sh
./compile_papers.sh
```

Or compile manually:

```bash
cd docs/
pdflatex FarmifAI_Paper_EN.tex
pdflatex FarmifAI_Paper_EN.tex  # Run twice for references
pdflatex FarmifAI_Paper_ES.tex
pdflatex FarmifAI_Paper_ES.tex
```

### Output

After compilation:
- `FarmifAI_Paper_EN.pdf` - English version (~15 pages)
- `FarmifAI_Paper_ES.pdf` - Spanish version (~15 pages)

## Paper Structure

Both papers include:

1. **Abstract** - Summary of the system and contributions
2. **Introduction** - Problem statement and contributions
3. **System Architecture** - Overview and technology stack
4. **Vision Model** - Implementation, training, inference, deployment
5. **NLP Model** - Semantic search and RAG implementation
6. **LLM** - Llama 3.2 integration and inference
7. **Voice Interface** - Vosk STT implementation
8. **Results** - Performance metrics and evaluation
9. **Deployment Workflow** - Complete deployment process
10. **Conclusion** - Summary and future work

## Quick Online Compilation

If you don't want to install LaTeX locally, use:

1. **Overleaf**: Upload `.tex` files and diagrams to [overleaf.com](https://overleaf.com)
2. **LaTeX.Online**: Use [latex.online](https://latexonline.cc/)

## File Dependencies

The LaTeX files expect the following diagrams in the same directory:
- `fig_system_architecture.png`
- `fig_training_architecture.png`
- `fig_rag_pipeline.png`
- `fig_vision_inference.png`
- `fig_two_phase_training.png`
- `fig_deployment_workflow.png`

Make sure to run `generate_diagrams.py` before compiling the papers.
