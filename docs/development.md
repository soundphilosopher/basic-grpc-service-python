# 🔧 Development Guide

Welcome to the development guide! Here's everything you need to know about contributing to and developing the Basic gRPC Service.

## 🛠️ Development Setup

### Prerequisites

- **Python 3.10+**
- **buf CLI** (optional, for protobuf management)
- **mkcert** for local TLS certificates
- **grpcurl** for testing

### Environment Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd basic-grpc-service-python

# Set up Python path for development
export PYTHONPATH="$PYTHONPATH:$(pwd):$(pwd)/sdk:$(pwd)/services:$(pwd)/utils"

# Install in development mode
python -m pip install -e .

# Install development dependencies
pip install -e ".[dev,docs]"
```

## 📦 Project Structure

```
basic-grpc-service-python/
├── 📁 proto/                    # Protocol Buffer definitions
│   ├── basic/v1/basic.proto     # Main service definitions
│   └── basic/service/v1/        # Message types and events
├── 📁 sdk/                      # Generated Python code
│   ├── basic/                   # Auto-generated from protos
│   └── cloudevents/             # CloudEvents protobuf
├── 📁 services/                 # Service implementations
│   ├── __init__.py              # Package initialization
│   └── basic_service.py         # Main service logic
├── 📁 utils/                    # Utility modules
│   ├── __init__.py              # Package exports
│   ├── eliza.py                 # Eliza chatbot implementation
│   └── some.py                  # Helper utilities
├── 📁 docs/                     # MkDocs documentation
├── 📁 certs/                    # TLS certificates
├── 🐍 server.py                 # Main server entry point
├── 📋 pyproject.toml            # Python project configuration
├── 🛡️ buf.yaml                  # Buf configuration
└── ⚙️ buf.gen.yaml              # Code generation config
```

## 🔄 Code Generation

This project uses [Buf](https://buf.build/) for protobuf management and code generation.

### Regenerating Python Code

When you modify `.proto` files, regenerate the Python code:

```bash
# Using buf (recommended)
buf generate

# Or using protoc directly (if you don't have buf)
protoc --python_out=sdk --pyi_out=sdk --grpc_python_out=sdk proto/basic/v1/*.proto
```

### Generated Files

The code generation creates:
- **Regular Python modules** (`*_pb2.py`)
- **gRPC service stubs** (`*_pb2_grpc.py`)
- **Type stubs** (`*.pyi`) for better IDE support
- **Package `__init__.py` files** automatically

## 🧪 Testing

### Manual Testing with grpcurl

```bash
# Start the server
python server.py

# Test the services
grpcurl -insecure -d '{"message": "test"}' 127.0.0.1:8443 basic.v1.BasicService/Hello
```

### Health Checks

```bash
# Server health
grpcurl -insecure 127.0.0.1:8443 grpc.health.v1.Health/Check

# Service-specific health
grpcurl -insecure -d '{"service": "basic.v1.BasicService"}' \
  127.0.0.1:8443 grpc.health.v1.Health/Check
```

## 📚 Documentation Development

This project uses MkDocs with the Material theme for documentation.

### Building Documentation

```bash
# Install documentation dependencies
pip install mkdocs mkdocs-material mkdocstrings[python] mkdocs-gen-files mkdocs-literate-nav mkdocs-section-index

# Serve documentation locally
mkdocs serve

# Build static documentation
mkdocs build
```

### Documentation Structure

- **`docs/`** - Markdown documentation files
- **`docs/gen_ref_pages.py`** - Auto-generates API reference from docstrings
- **`mkdocs.yml`** - MkDocs configuration

### Writing Documentation

- Use **emoji** for visual appeal 🎨
- Include **code examples** with proper syntax highlighting
- Add **cross-references** between sections
- Keep it **conversational** but professional

## 🎨 Code Style

### Docstring Style

We use a fun, engaging docstring style with emojis and personality:

```python
def example_function(param: str) -> str:
    """
    🎉 This function does something awesome!

    A detailed description of what this function does, why it exists,
    and how it fits into the bigger picture. Include personality and
    make it fun to read!

    Args:
        param (str): Description of the parameter with examples

    Returns:
        str: What gets returned and when

    Raises:
        ValueError: When something goes wrong and why

    Example:
        >>> result = example_function("test")
        >>> print(result)
        "processed: test"

    Note:
        Any important notes, warnings, or tips for users!
    """
```

### Type Hints

- Use **type hints** everywhere
- Import types from `typing` when needed
- Use **generic types** for containers (`List[str]`, `Dict[str, Any]`)

## 🐛 Debugging

### Logging

The server uses structured JSON logging:

```python
import logging
logging.info("Something happened", extra={"key": "value"})
```

### Common Issues

1. **Import Errors**: Make sure `PYTHONPATH` includes all necessary directories
2. **Certificate Issues**: Regenerate with `mkcert`
3. **Port Conflicts**: Check if port 8443 is already in use

### Python Path Issues

For pydoc and development:

```bash
export PYTHONPATH="$PYTHONPATH:$(pwd):$(pwd)/sdk:$(pwd)/services:$(pwd)/utils"
```

## 🚀 Deployment

### Building for Production

```bash
# Build documentation
mkdocs build

# The documentation will be in site/
```

### GitHub Pages Deployment

```bash
# Deploy documentation to GitHub Pages
mkdocs gh-deploy
```

## 🤝 Contributing

1. **Fork** the repository
2. **Create** a feature branch
3. **Make** your changes with proper documentation
4. **Test** your changes thoroughly
5. **Submit** a pull request

### Pull Request Guidelines

- Include **clear descriptions** of changes
- Add **documentation** for new features
- Maintain the **fun, engaging tone** in docstrings
- Test with both **pydoc** and **MkDocs**

Ready to contribute? The codebase is designed to be approachable and fun to work with! 🎉
