#!/bin/bash
# 📚 Quick deploy script for MkDocs documentation

set -e

echo " Setting up MkDocs documentation..."

# Install documentation dependencies
echo " Installing documentation dependencies..."
pip install -e ".[docs]"

# Set up Python path
export PYTHONPATH="$PYTHONPATH:$(pwd):$(pwd)/sdk:$(pwd)/services:$(pwd)/utils"

# Build and serve documentation
echo "󱥊 Building documentation..."
mkdocs build

echo "󰖟 Deploy to github ..."
echo "  Documentation will be available at: https://soundphilosopher.github.io/basic-grpc-service-python/"

mkdocs gh-deploy
