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

# Add alias to bashrc for convenience
echo ""
echo "Setting up ai-dev alias in ~/.bashrc..."
ALIAS_LINE="alias ai-dev='source $(pwd)/venv/bin/activate && ai-dev'"
if ! grep -q "alias ai-dev=" ~/.bashrc; then
    echo "$ALIAS_LINE" >> ~/.bashrc
    echo "✅ Alias added to ~/.bashrc"
else
    echo "ℹ️  Alias already exists in ~/.bashrc"
fi

echo ""
echo "========================================="
echo "Setup completed successfully!"
echo "========================================="
echo ""
echo "The ai-dev alias has been added to your ~/.bashrc"
echo ""
echo "To start using ai-dev immediately, run:"
echo "  source ~/.bashrc && ai-dev --help"
echo ""
echo "Or restart your terminal for the changes to take effect."
echo ""
echo "Alternative: activate the virtual environment manually:"
echo "  source venv/bin/activate"
echo "  ai-dev --help"
echo ""

# Ask user if they want to test ai-dev now
echo "Would you like to test ai-dev now? (Y/n): "
read -r response
if [[ "$response" =~ ^([yY][eE][sS]|[yY]|)$ ]]; then
    echo ""
    echo "Please run the following command to test ai-dev:"
    echo "  source ~/.bashrc && ai-dev status"
    echo ""
    echo "Copy and paste the command above to test."
fi