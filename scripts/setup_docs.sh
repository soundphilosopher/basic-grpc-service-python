#!/bin/bash
# File: basic-grpc-service-python/setup_docs.sh
# 📚 Quick setup script for MkDocs documentation

set -e

echo "🚀 Setting up MkDocs documentation..."

# Create docs directory if it doesn't exist
mkdir -p docs

# Install documentation dependencies
echo "📦 Installing documentation dependencies..."
pip install -e ".[docs]"

# Set up Python path
export PYTHONPATH="$PYTHONPATH:$(pwd):$(pwd)/sdk:$(pwd)/services:$(pwd)/utils"

# Build and serve documentation
echo "🏗️ Building documentation..."
mkdocs build

echo "🌐 Starting documentation server..."
echo "📖 Documentation will be available at: http://127.0.0.1:8000"
echo "🛑 Press Ctrl+C to stop the server"

mkdocs serve
