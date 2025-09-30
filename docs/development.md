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

# Install in development mode with all dependencies
python -m pip install -e ".[dev,docs]"

# Generate TLS certificates
mkcert -cert-file ./certs/local.crt -key-file ./certs/local.key localhost 127.0.0.1
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
├── 📁 tests/                    # 🧪 Comprehensive test suite
│   ├── conftest.py              # pytest fixtures and configuration
│   ├── test_eliza.py            # Eliza chatbot tests (40+ cases)
│   ├── test_basic_service.py    # gRPC service tests (40+ cases)
│   └── htmlcov/                 # Coverage reports (generated)
├── 📁 docs/                     # MkDocs documentation
├── 📁 scripts/                  # Development automation
│   ├── run_tests.sh             # 🧪 Enhanced test runner
│   ├── setup_docs.sh            # Documentation setup
│   └── gen_ref_pages.py         # API reference generation
├── 📁 certs/                    # TLS certificates
├── 🐍 server.py                 # Main server entry point
├── 📋 pyproject.toml            # Python project configuration
├── 🛡️ buf.yaml                  # Buf configuration
└── ⚙️ buf.gen.yaml              # Code generation config
```

## 🧪 Testing Workflow

### Quick Testing

```bash
# Run all tests with our enhanced runner
./scripts/run_tests.sh

# Run with coverage reporting
./scripts/run_tests.sh --coverage

# Fast runs during development (skip dependency install)
./scripts/run_tests.sh --fast
```

### Manual Testing Commands

```bash
# Run specific test files
python -m pytest tests/test_eliza.py -v
python -m pytest tests/test_basic_service.py -v --asyncio-mode=auto

# Run specific test classes or methods
python -m pytest tests/test_basic_service.py::TestHelloMethod -v
python -m pytest tests/test_eliza.py::TestGoodbyeDetection::test_goodbye_simple -v

# Debug failing tests with maximum verbosity
python -m pytest tests/test_basic_service.py::TestBackgroundMethod -vvv -s
```

### Test Coverage Requirements

- **Services** (`services/`) → **95%+** coverage required
- **Utils** (`utils/`) → **90%+** coverage required
- **Overall project** → **90%+** coverage required

```bash
# Check coverage
./scripts/run_tests.sh --coverage

# View detailed HTML coverage report
python -m http.server 8000 -d htmlcov/
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

## 🧪 Manual Service Testing

### Start the Development Server

```bash
# Start the server with debug logging
python server.py
```

### Testing with grpcurl

```bash
# Test the Hello method
grpcurl -insecure -d '{"message": "test"}' 127.0.0.1:8443 basic.v1.BasicService/Hello

# Test bidirectional streaming (Talk)
echo '{"message": "Hello Eliza"}' | \
  grpcurl -insecure -d @ 127.0.0.1:8443 basic.v1.BasicService/Talk

# Test server streaming (Background)
grpcurl -insecure -d '{"processes": 3}' \
  127.0.0.1:8443 basic.v1.BasicService/Background
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
# Install documentation dependencies (already included in [docs])
pip install -e ".[docs]"

# Serve documentation locally with hot reload
mkdocs serve

# Build static documentation
mkdocs build

# Deploy to GitHub Pages
mkdocs gh-deploy
```

### Documentation Structure

- **`docs/`** - Markdown documentation files
- **`docs/testing.md`** - 🧪 Comprehensive testing guide
- **`scripts/gen_ref_pages.py`** - Auto-generates API reference from docstrings
- **`mkdocs.yml`** - MkDocs configuration

### Writing Documentation

- Use **emoji** for visual appeal 🎨
- Include **code examples** with proper syntax highlighting
- Add **cross-references** between sections
- Keep it **conversational** but professional
- Test all code examples in documentation

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

### Testing Standards

- **Descriptive test names**: `test_hello_with_empty_message_returns_valid_response`
- **Test behavior, not implementation**: Focus on what the code should do
- **Include edge cases**: Empty inputs, special characters, error conditions
- **Use proper async patterns**: `@pytest.mark.asyncio` for async tests
- **Mock external dependencies**: Use `AsyncMock` for gRPC contexts

## 🐛 Debugging

### Logging

The server uses structured JSON logging:

```python
import logging
logging.info("Something happened", extra={"key": "value"})
```

### Common Issues

1. **Import Errors**: Make sure `PYTHONPATH` includes all necessary directories
   ```bash
   export PYTHONPATH="$PYTHONPATH:$(pwd):$(pwd)/sdk:$(pwd)/services:$(pwd)/utils"
   ```

2. **Certificate Issues**: Regenerate with `mkcert`
   ```bash
   mkcert -cert-file ./certs/local.crt -key-file ./certs/local.key localhost 127.0.0.1
   ```

3. **Port Conflicts**: Check if port 8443 is already in use
   ```bash
   lsof -ti:8443 | xargs kill -9
   ```

4. **Test Failures**: Use our enhanced test runner for debugging
   ```bash
   ./scripts/run_tests.sh --verbose
   ```

### Debugging Tests

```bash
# Run specific failing test with maximum detail
python -m pytest tests/test_basic_service.py::TestBackgroundMethod::test_background_timestamps -vvv -s

# Use Python debugger
python -m pytest tests/test_eliza.py --pdb

# Check test discovery
python -m pytest --collect-only
```

## 🚀 Deployment

### Pre-deployment Checklist

```bash
# 1. All tests must pass
./scripts/run_tests.sh --coverage

# 2. Coverage should be above 90%
# (Check the coverage report output)

# 3. Documentation should build successfully
mkdocs build

# 4. Manual testing should work
python server.py
# Test with grpcurl...

# 5. No linting errors
# (Add your preferred linter here)
```

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

### Development Workflow

1. **Fork** the repository
2. **Create** a feature branch
3. **Set up** development environment
4. **Make** your changes with proper documentation
5. **Write tests** for new functionality
6. **Run test suite** and ensure all pass
7. **Update documentation** if needed
8. **Submit** a pull request

### Pull Request Guidelines

- Include **clear descriptions** of changes
- Add **comprehensive tests** for new features
- Maintain **90%+ test coverage**
- Update **documentation** for new features
- Maintain the **fun, engaging tone** in docstrings
- Test with both **pytest** and **MkDocs**
- All tests must pass: `./scripts/run_tests.sh --coverage`

### Code Review Checklist

**For Reviewers:**
- ✅ All tests pass
- ✅ Coverage remains above 90%
- ✅ Documentation updated
- ✅ Code follows project style
- ✅ No breaking changes (or properly documented)

**For Contributors:**
- ✅ Self-review your changes
- ✅ Run full test suite locally
- ✅ Update relevant documentation
- ✅ Test examples in documentation work
- ✅ Check that new features are properly tested

## 🎯 Development Tips

### Efficient Development Loop

```bash
# 1. Make code changes
# 2. Run tests quickly
./scripts/run_tests.sh --fast

# 3. For major changes, run full test suite
./scripts/run_tests.sh --coverage

# 4. Test manually if needed
python server.py
grpcurl -insecure -d '{"message": "test"}' 127.0.0.1:8443 basic.v1.BasicService/Hello
```

### IDE Setup Tips

- **Set PYTHONPATH** in your IDE to include `sdk`, `services`, `utils`
- **Enable type checking** for better development experience
- **Configure pytest** as your test runner with `--asyncio-mode=auto`

Ready to contribute? The codebase is designed to be approachable and fun to work with! 🎉

For detailed testing information, check out our comprehensive [Testing Guide](testing.md)!
