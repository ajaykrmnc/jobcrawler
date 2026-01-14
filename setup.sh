#!/bin/bash

# Job Automation Setup Script

echo "=========================================="
echo "Job Automation System - Setup"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "✅ Dependencies installed successfully!"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your configuration:"
    echo "   - Add your Gemini API key"
    echo "   - Configure SMTP settings"
    echo "   - Add your RSS feed URLs"
    echo "   - Set your profile information"
    echo ""
else
    echo "✅ .env file already exists"
    echo ""
fi

echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file with your configuration"
echo "2. Test locally: python main.py"
echo "3. Push to GitHub and configure secrets"
echo "4. Enable GitHub Actions"
echo ""
echo "To activate the virtual environment in the future:"
echo "  source venv/bin/activate"
echo ""

