#!/bin/bash

# AI Dev Tool - Virtual Environment Activation Script
# This script helps activate the virtual environment and run ai-dev

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo ""
    echo "Please run setup.sh first:"
    echo "  bash setup.sh"
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if ai-dev is installed
if ! command -v ai-dev &> /dev/null; then
    echo "❌ ai-dev command not found in virtual environment!"
    echo ""
    echo "Installing ai-dev..."
    pip install -e .
fi

# Display status
echo "✅ Virtual environment activated!"
echo ""
echo "You can now use ai-dev commands:"
echo "  ai-dev --help"
echo "  ai-dev status"
echo ""
echo "To deactivate the virtual environment, run:"
echo "  deactivate"