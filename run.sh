#!/bin/bash

# LangGraph Adventure Agent - Run Script
# This script provides convenient commands for running and managing the LangGraph project

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo -e "${RED}Error: Virtual environment not found.${NC}"
    echo "Please run: uv venv"
    exit 1
fi

# Activate virtual environment
source .venv/bin/activate

# Load environment variables from .env file if it exists
if [ -f ".env" ]; then
    set -a
    source .env
    set +a
fi

# Function to print usage
usage() {
    echo "Usage: ./run.sh [command]"
    echo ""
    echo "Commands:"
    echo "  dev          Run LangGraph development server"
    echo "  dev-tunnel   Run dev server with public tunnel (Cloudflare)"
    echo "  test         Run tests"
    echo "  lint         Run linting checks"
    echo "  typecheck    Run type checking"
    echo "  install      Install/update dependencies"
    echo "  build        Build Docker image"
    echo "  clean        Clean build artifacts"
    echo "  help         Show this help message"
    echo ""
    echo "Examples:"
    echo "  ./run.sh dev"
    echo "  ./run.sh dev --port 8000"
    echo "  ./run.sh test"
}

# Parse command
COMMAND="${1:-help}"

case "$COMMAND" in
    dev)
        echo -e "${GREEN}Starting LangGraph development server...${NC}"
        shift
        langgraph dev "$@"
        ;;
    
    dev-tunnel)
        echo -e "${GREEN}Starting LangGraph development server with tunnel...${NC}"
        shift
        langgraph dev --tunnel "$@"
        ;;
    
    test)
        echo -e "${GREEN}Running tests...${NC}"
        if [ ! -f ".venv/bin/pytest" ]; then
            echo -e "${YELLOW}Installing test dependencies...${NC}"
            uv pip install -e ".[dev]"
        fi
        pytest "${@:2}"
        ;;
    
    lint)
        echo -e "${GREEN}Running linting checks...${NC}"
        if [ ! -f ".venv/bin/ruff" ]; then
            echo -e "${YELLOW}Installing dev dependencies...${NC}"
            uv pip install -e ".[dev]"
        fi
        ruff check .
        ;;
    
    typecheck)
        echo -e "${GREEN}Running type checking...${NC}"
        if [ ! -f ".venv/bin/mypy" ]; then
            echo -e "${YELLOW}Installing dev dependencies...${NC}"
            uv pip install -e ".[dev]"
        fi
        mypy src/
        ;;
    
    install)
        echo -e "${GREEN}Installing/updating dependencies...${NC}"
        uv pip install -U "langgraph-cli[inmem]"
        uv pip install -e .
        echo -e "${GREEN}✓ Dependencies installed${NC}"
        ;;
    
    build)
        echo -e "${GREEN}Building Docker image...${NC}"
        langgraph build
        ;;
    
    clean)
        echo -e "${GREEN}Cleaning build artifacts...${NC}"
        rm -rf adventure_agent.egg-info
        rm -rf build
        rm -rf dist
        find . -type d -name __pycache__ -exec rm -r {} + 2>/dev/null || true
        find . -type f -name "*.pyc" -delete 2>/dev/null || true
        echo -e "${GREEN}✓ Cleaned${NC}"
        ;;
    
    help|--help|-h)
        usage
        ;;
    
    *)
        echo -e "${RED}Unknown command: $COMMAND${NC}"
        echo ""
        usage
        exit 1
        ;;
esac

