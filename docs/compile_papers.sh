#!/bin/bash
# FarmifAI Paper PDF Generation Script
# 
# Requirements:
#   sudo apt-get install texlive-latex-base texlive-latex-extra \
#       texlive-fonts-recommended texlive-lang-spanish
#
# Usage:
#   cd docs/
#   ./compile_papers.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== FarmifAI Paper Compilation ==="
echo ""

# Check for pdflatex
if ! command -v pdflatex &> /dev/null; then
    echo "ERROR: pdflatex not found!"
    echo ""
    echo "Please install LaTeX:"
    echo "  Ubuntu/Debian:"
    echo "    sudo apt-get install texlive-latex-base texlive-latex-extra \\"
    echo "        texlive-fonts-recommended texlive-lang-spanish"
    echo ""
    echo "  Fedora:"
    echo "    sudo dnf install texlive-scheme-medium texlive-babel-spanish"
    echo ""
    echo "  macOS:"
    echo "    brew install --cask mactex-no-gui"
    echo ""
    exit 1
fi

echo "Compiling English version..."
pdflatex -interaction=nonstopmode FarmifAI_Paper_EN.tex > /dev/null
pdflatex -interaction=nonstopmode FarmifAI_Paper_EN.tex > /dev/null
echo "  Created: FarmifAI_Paper_EN.pdf"

echo ""
echo "Compiling Spanish version..."
pdflatex -interaction=nonstopmode FarmifAI_Paper_ES.tex > /dev/null
pdflatex -interaction=nonstopmode FarmifAI_Paper_ES.tex > /dev/null
echo "  Created: FarmifAI_Paper_ES.pdf"

# Clean up auxiliary files
echo ""
echo "Cleaning up auxiliary files..."
rm -f *.aux *.log *.out *.toc *.lof *.lot *.fls *.fdb_latexmk 2>/dev/null || true

echo ""
echo "=== Compilation Complete ==="
echo ""
echo "Generated PDFs:"
ls -lh *.pdf 2>/dev/null || echo "  No PDFs found"
echo ""
echo "Generated diagrams:"
ls -lh *.png 2>/dev/null | head -6 || echo "  No diagrams found"
