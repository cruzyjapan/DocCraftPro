#!/bin/bash

# AI Dev Tool - Initialization Script
# This script sets up the complete development environment

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[*]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

# Header
echo ""
echo "================================================"
echo "   AI Dev Tool - Auto Initialization Script"
echo "================================================"
echo ""

# Check if running from correct directory
if [ ! -f "requirements.txt" ]; then
    print_error "Please run this script from the project root directory"
    exit 1
fi

# Step 1: Check Python version
print_status "Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    print_success "Python $PYTHON_VERSION found"
    
    # Check if version is 3.10 or higher
    if [ "$(echo "$PYTHON_VERSION >= 3.10" | bc -l)" -eq 0 ]; then
        print_error "Python 3.10 or higher is required (found $PYTHON_VERSION)"
        exit 1
    fi
else
    print_error "Python3 is not installed"
    exit 1
fi

# Step 2: Check and install python3-venv if needed
print_status "Checking python3-venv..."
if ! python3 -m venv --help &> /dev/null; then
    print_warning "python3-venv is not installed"
    print_status "Installing python3-venv (sudo password may be required)..."
    
    # Detect Python version for package name
    PYTHON_MAJOR_MINOR=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
    
    if command -v apt &> /dev/null; then
        sudo apt update
        sudo apt install -y python${PYTHON_MAJOR_MINOR}-venv
    elif command -v yum &> /dev/null; then
        sudo yum install -y python3-venv
    elif command -v dnf &> /dev/null; then
        sudo dnf install -y python3-venv
    else
        print_error "Could not install python3-venv automatically. Please install it manually."
        exit 1
    fi
    print_success "python3-venv installed"
else
    print_success "python3-venv is available"
fi

# Step 3: Create virtual environment
print_status "Creating virtual environment..."
if [ -d "venv" ]; then
    print_warning "Virtual environment already exists"
    read -p "Do you want to recreate it? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf venv
        python3 -m venv venv
        print_success "Virtual environment recreated"
    else
        print_status "Using existing virtual environment"
    fi
else
    python3 -m venv venv
    print_success "Virtual environment created"
fi

# Step 4: Activate virtual environment and install dependencies
print_status "Installing dependencies..."
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip --quiet

# Install requirements
pip install -r requirements.txt --quiet
print_success "Dependencies installed"

# Step 5: Install package in development mode
print_status "Installing ai-dev-tool in development mode..."
pip install -e . --quiet
print_success "ai-dev-tool installed"

# Step 6: Create necessary directories
print_status "Creating project directories..."
mkdir -p output
mkdir -p templates
mkdir -p tests
print_success "Directories created"

# Step 7: Initialize configuration if not exists
print_status "Initializing configuration..."
if [ ! -f "config/default.yaml" ]; then
    # Create config directory if not exists
    mkdir -p config
    
    # Initialize using the CLI
    python3 -m ai_dev.cli init --force
    print_success "Configuration initialized"
else
    print_warning "Configuration already exists (config/default.yaml)"
fi

# Step 8: Create sample input files for testing
print_status "Creating sample files..."
cat > sample_input.txt << 'EOF'
オンラインショッピングサイトの開発

以下の機能を実装する必要があります：
1. ユーザー登録・ログイン機能
2. 商品検索・一覧表示
3. ショッピングカート機能
4. 注文処理と決済
5. 注文履歴の確認
6. 管理者用ダッシュボード

セキュリティとパフォーマンスを重視した設計にしてください。
EOF

cat > sample_input_en.txt << 'EOF'
Online Shopping Site Development

The following features need to be implemented:
1. User registration and login functionality
2. Product search and listing
3. Shopping cart functionality
4. Order processing and payment
5. Order history viewing
6. Administrator dashboard

Please design with emphasis on security and performance.
EOF

print_success "Sample files created (sample_input.txt, sample_input_en.txt)"

# Step 9: Check AI CLI availability
print_status "Checking AI CLI tools..."
echo ""

if command -v gemini &> /dev/null; then
    print_success "Gemini CLI is installed"
    GEMINI_VERSION=$(gemini --version 2>&1 || echo "version unknown")
    echo "    Version: $GEMINI_VERSION"
else
    print_warning "Gemini CLI is not installed or not in PATH"
    echo "    To use Gemini, install it from: https://gemini.google.com/cli"
fi

if command -v claude-code &> /dev/null; then
    print_success "Claude Code CLI is installed"
    CLAUDE_VERSION=$(claude-code --version 2>&1 || echo "version unknown")
    echo "    Version: $CLAUDE_VERSION"
else
    print_warning "Claude Code CLI is not installed or not in PATH"
    echo "    To use Claude, install it from: https://docs.anthropic.com/claude-code"
fi

echo ""

# Step 10: Create convenience scripts
print_status "Creating convenience scripts..."

# Create activation script
cat > activate.sh << 'EOF'
#!/bin/bash
# Activate virtual environment
source venv/bin/activate
echo "Virtual environment activated. Use 'deactivate' to exit."
EOF
chmod +x activate.sh

# Create quick test script
cat > test_tool.sh << 'EOF'
#!/bin/bash
# Quick test of the AI Dev Tool

source venv/bin/activate

echo "Testing AI Dev Tool..."
echo ""

# Show status
ai-dev status

echo ""
echo "Generating sample requirements..."
ai-dev generate requirements sample_input.txt -o output/test_requirements.md

echo ""
echo "Test completed. Check output/test_requirements.md"
EOF
chmod +x test_tool.sh

print_success "Convenience scripts created (activate.sh, test_tool.sh)"

# Final summary
echo ""
echo "================================================"
echo "   Installation Completed Successfully!"
echo "================================================"
echo ""
echo "Quick Start Guide:"
echo ""
echo "1. Activate virtual environment:"
echo "   ${GREEN}source venv/bin/activate${NC}"
echo "   or use: ${GREEN}./activate.sh${NC}"
echo ""
echo "2. Check tool status:"
echo "   ${GREEN}ai-dev status${NC}"
echo ""
echo "3. View help:"
echo "   ${GREEN}ai-dev --help${NC}"
echo ""
echo "4. Generate your first document:"
echo "   ${GREEN}ai-dev generate requirements sample_input.txt${NC}"
echo ""
echo "5. Run a quick test:"
echo "   ${GREEN}./test_tool.sh${NC}"
echo ""

if ! command -v gemini &> /dev/null && ! command -v claude-code &> /dev/null; then
    echo "================================================"
    print_warning "No AI CLI tools detected!"
    echo ""
    echo "To use this tool, you need to install at least one of:"
    echo "  - Gemini CLI"
    echo "  - Claude Code CLI"
    echo ""
    echo "The tool will still work but will show warnings"
    echo "when trying to execute AI commands."
    echo "================================================"
fi

echo ""
print_success "Setup complete! Your environment is ready."
echo ""

# Optionally activate the environment
read -p "Do you want to activate the virtual environment now? (Y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Nn]$ ]]; then
    echo ""
    print_status "Activating virtual environment..."
    echo "Run 'deactivate' to exit the virtual environment"
    echo ""
    exec bash --init-file <(echo "source venv/bin/activate")
fi