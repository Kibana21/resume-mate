#!/bin/bash

# Installation script for Resume Mate dependencies

echo "========================================"
echo "Installing Resume Mate Dependencies"
echo "========================================"
echo ""

# Check if virtual environment is activated
if [[ -z "${VIRTUAL_ENV}" ]]; then
    echo "⚠️  No virtual environment detected."
    echo "It's recommended to use a virtual environment."
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Installation cancelled."
        exit 1
    fi
fi

echo "📦 Installing core dependencies..."
pip install pydantic>=2.6.0 pydantic-settings>=2.0.0

echo "📦 Installing DSPy and OpenAI..."
pip install dspy-ai>=2.4.0 openai>=1.12.0

echo "📦 Installing document parsers..."
pip install pdfplumber>=0.10.0 python-docx>=1.1.0

echo "📦 Installing utilities..."
pip install loguru>=0.7.2 python-dotenv>=1.0.0

echo ""
echo "✅ Core dependencies installed!"
echo ""
echo "Optional: Install additional dependencies for full functionality"
echo "  pip install -r requirements.txt"
echo ""
echo "Next steps:"
echo "  1. Configure .env file with Azure OpenAI credentials"
echo "  2. Place resume.pdf in data/sample_cvs/"
echo "  3. Run: python scripts/extract_cv.py data/sample_cvs/resume.pdf"
echo ""
