#!/bin/bash
# McswazSting AI Manager - Termux Setup Script
# Automated environment configuration for mobile Termux deployment

set -e

echo "═══════════════════════════════════════════���═══════════════════"
echo "McswazSting AI Manager - Termux Installation Script"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}[1/6]${NC} Updating package repositories...
apt update
apt upgrade -y

echo -e "${BLUE}[2/6]${NC} Installing Python 3 and build tools...
apt install -y python python-pip clang git build-essential

echo -e "${BLUE}[3/6]${NC} Installing Node.js and npm...
apt install -y nodejs npm

echo -e "${BLUE}[4/6]${NC} Setting up storage permissions...
if [ ! -d "$HOME/storage" ]; then
    termux-setup-storage
    echo -e "${GREEN}Storage permissions configured${NC}"
else
    echo -e "${GREEN}Storage already configured${NC}"
fi

echo -e "${BLUE}[5/6]${NC} Installing Python dependencies from requirements.txt...
if [ -f "backend/requirements.txt" ]; then
    pip install --upgrade pip setuptools wheel
    pip install -r backend/requirements.txt
    echo -e "${GREEN}Python dependencies installed${NC}"
else
    echo -e "${YELLOW}Warning: requirements.txt not found${NC}"
fi

echo -e "${BLUE}[6/6]${NC} Creating logs directory...
mkdir -p logs
chmod 755 logs

echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✓ Installation Complete!${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
echo ""
echo "Next steps:"
echo "1. Start the Flask server: python backend/server.py"
echo "2. Access the API at: http://localhost:5000"
echo "3. Check /api/status endpoint"
echo ""
echo "Environment Details:"
echo "- Python: $(python --version)"
echo "- Node: $(node --version)"
echo "- NPM: $(npm --version)"
echo ""
