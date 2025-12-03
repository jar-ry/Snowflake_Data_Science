#!/bin/bash
# =============================================================================
# Snowflake Data Science Environment Setup Script
# =============================================================================
# This script creates a conda environment from conda.yml for the 
# Retail CLV Regression Demo project.
# =============================================================================

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Environment name (from conda.yml)
ENV_NAME="snowflake_ds"

echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}  Snowflake Data Science Environment Setup${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""

# Check if conda is installed
if ! command -v conda &> /dev/null; then
    echo -e "${RED}Error: conda is not installed or not in PATH${NC}"
    echo "Please install Miniconda or Anaconda first:"
    echo "  https://docs.conda.io/en/latest/miniconda.html"
    exit 1
fi

echo -e "${GREEN}✓ Conda found${NC}"

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
CONDA_YML="${SCRIPT_DIR}/conda.yml"

# Check if conda.yml exists
if [ ! -f "$CONDA_YML" ]; then
    echo -e "${RED}Error: conda.yml not found at ${CONDA_YML}${NC}"
    exit 1
fi

echo -e "${GREEN}✓ conda.yml found${NC}"

# Check if environment already exists
if conda env list | grep -q "^${ENV_NAME} "; then
    echo -e "${YELLOW}Environment '${ENV_NAME}' already exists.${NC}"
    read -p "Do you want to remove and recreate it? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}Removing existing environment...${NC}"
        conda env remove -n "$ENV_NAME" -y
    else
        echo -e "${BLUE}Keeping existing environment.${NC}"
        echo ""
        echo -e "${GREEN}To activate the environment, run:${NC}"
        echo -e "  ${YELLOW}conda activate ${ENV_NAME}${NC}"
        exit 0
    fi
fi

# Create the conda environment
echo ""
echo -e "${BLUE}Creating conda environment '${ENV_NAME}'...${NC}"
echo -e "${YELLOW}This may take a few minutes...${NC}"
echo ""

conda env create -f "$CONDA_YML"

# Check if creation was successful
if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}================================================${NC}"
    echo -e "${GREEN}  Environment created successfully!${NC}"
    echo -e "${GREEN}================================================${NC}"
    echo ""
    echo -e "To activate the environment, run:"
    echo -e "  ${YELLOW}conda activate ${ENV_NAME}${NC}"
    echo ""
    echo -e "To start JupyterLab, run:"
    echo -e "  ${YELLOW}conda activate ${ENV_NAME} && jupyter lab${NC}"
    echo ""
    echo -e "To deactivate the environment, run:"
    echo -e "  ${YELLOW}conda deactivate${NC}"
    echo ""
else
    echo -e "${RED}Error: Failed to create conda environment${NC}"
    exit 1
fi

