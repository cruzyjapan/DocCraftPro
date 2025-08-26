#!/bin/bash

# AI Dev Tool Setup Script

echo "========================================="
echo "AI Dev Tool - Setup Script"
echo "========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version

# Install python3-venv if needed
echo ""
echo "Installing python3-venv package..."
echo "Please enter your password if prompted:"
sudo apt update
sudo apt install -y python3.12-venv

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Install package in development mode
echo ""
echo "Installing ai-dev-tool in development mode..."
pip install -e .

# Initialize configuration
echo ""
echo "Initializing configuration..."
python3 -m ai_dev.cli init

echo ""
echo "========================================="
echo "Setup completed successfully!"
echo "========================================="
echo ""
echo "To activate the virtual environment, run:"
echo "  source venv/bin/activate"
echo ""
echo "To get started, try:"
echo "  ai-dev status"
echo "  ai-dev --help"
echo ""