# 🚀 Getting Started

Get up and running with the Basic gRPC Service in just a few minutes!

## 📋 Prerequisites

Before we begin, make sure you have:

- **Python 3.10+** (because we love modern Python! 🐍)
- **pip** for package management
- **mkcert** for generating local TLS certificates

## 🔧 Installation

### 1. Generate TLS Certificates

First, let's create some local certificates for secure communication:

```bash
# Install mkcert (choose your platform)
# macOS: brew install mkcert
# Windows: choco install mkcert
# Linux: check your package manager

# Install the local Certificate Authority
mkcert -install

# Generate certificates for localhost
mkdir -p certs
mkcert -cert-file ./certs/local.crt -key-file ./certs/local.key localhost 127.0.0.1 0.0.0.0 ::1
```

### 2. Install Dependencies

```bash
# Install the project in development mode
python -m pip install -e .

# For development with testing (recommended)
python -m pip install -e ".[dev]"

# For documentation development
python -m pip install -e ".[docs]"
```

This will install all required dependencies including gRPC, protobuf, logging libraries, and testing tools.

### 3. Set Up Python Path

For development and documentation generation, set up your Python path:

```bash
export PYTHONPATH="$PYTHONPATH:$(pwd):$(pwd)/sdk:$(pwd)/services:$(pwd)/utils"
```

## 🎬 Running the Server

Start the gRPC server:

```bash
python server.py
```

You should see JSON-formatted log output indicating the server is running:

```json
{"level": "INFO", "message": "gRPC server listening on https://127.0.0.1:8443 (HTTP/2)", "time": "2024-01-01T12:00:00.000Z"}
```

The server is now running on `https://127.0.0.1:8443` with TLS encryption! 🔐

## 🧪 Verify Installation (Testing)

Make sure everything works correctly with our comprehensive test suite:

```bash
# Run all tests (80+ test cases)
./scripts/run_tests.sh

# Run with coverage reporting to see what's tested
./scripts/run_tests.sh --coverage
```

You should see output like:
```bash
🧪 Basic gRPC Service Test Runner
==================================

📦 Installing dependencies...
✅ Dependencies installed

🔍 Discovering tests...
Found 2 test files:
  📄 tests/test_eliza.py
  📄 tests/test_basic_service.py

🏗️ Running tests...
Command: python -m pytest tests/ --asyncio-mode=auto -v

🎉 All tests passed!
✅ Test suite completed successfully!
Your gRPC service is ready for production! 🚀
```

### What Gets Tested

Our test suite covers:
- ✅ **Eliza Chatbot** (40+ tests) - Pattern matching, conversations, edge cases
- ✅ **gRPC Service** (40+ tests) - All methods, streaming, CloudEvents, errors
- ✅ **Integration** - Components working together
- ✅ **Edge Cases** - Empty inputs, special characters, error conditions

## 🎮 Testing the Service

### Using grpcurl

[grpcurl](https://github.com/fullstorydev/grpcurl) is the best way to test gRPC services:

```bash
# Discover services
grpcurl -insecure 127.0.0.1:8443 list

# Say hello
grpcurl -insecure -d '{"message": "World"}' \
  127.0.0.1:8443 basic.v1.BasicService/Hello

# Start a conversation
grpcurl -insecure -d '{"message": "Hello!"}' \
  127.0.0.1:8443 basic.v1.BasicService/Talk

# Run background tasks
grpcurl -insecure -d '{"processes": 3}' \
  127.0.0.1:8443 basic.v1.BasicService/Background
```

### Health Checks

The server includes built-in health checking:

```bash
# Check overall health
grpcurl -insecure 127.0.0.1:8443 grpc.health.v1.Health/Check

# Check specific service
grpcurl -insecure -d '{"service": "basic.v1.BasicService"}' \
  127.0.0.1:8443 grpc.health.v1.Health/Check
```

## 🐍 Python Client Example

Create a simple client to interact with your service:

```python
import asyncio
import grpc
from basic.v1 import basic_pb2_grpc
from basic.service.v1 import service_pb2

async def main():
    # Connect to the server (insecure for local dev)
    channel = grpc.aio.insecure_channel('127.0.0.1:8443')
    stub = basic_pb2_grpc.BasicServiceStub(channel)

    try:
        # Call the Hello method
        request = service_pb2.HelloRequest(message="Python Client")
        response = await stub.Hello(request)
        print(f"Response: {response}")

    finally:
        await channel.close()

if __name__ == "__main__":
    asyncio.run(main())
```

## 🎯 Next Steps

Now that you have the service running and tested:

- 🧪 **[Testing Guide](testing.md)** - Learn about our comprehensive test suite
- 📖 **[API Reference](reference/)** - Understand all available methods
- 💬 **[Talk service](reference/services.basic_service.md#talk)** - Try real-time chat with Eliza
- 🏃‍♂️ **[Background service](reference/services.basic_service.md#background)** - Test parallel processing
- 🧠 **[Eliza chatbot](reference/utils.eliza.md)** - Learn about the AI therapist
- 🎮 **[Examples](examples.md)** - More advanced usage patterns
- 🔧 **[Development](development.md)** - Contributing and advanced development

## 🐛 Troubleshooting

### Common Issues

#### Installation Problems
```bash
# If pip install fails
python -m pip install --upgrade pip
python -m pip install -e ".[dev]" --force-reinstall
```

#### Certificate Issues
```bash
# If you get TLS certificate errors
rm certs/local.*
mkcert -cert-file ./certs/local.crt -key-file ./certs/local.key localhost 127.0.0.1
```

#### Test Failures
```bash
# If tests fail, run with verbose output
./scripts/run_tests.sh --verbose

# Or check specific test
python -m pytest tests/test_eliza.py -v
```

#### Import Errors
```bash
# Make sure PYTHONPATH is set
export PYTHONPATH="$PYTHONPATH:$(pwd):$(pwd)/sdk:$(pwd)/services:$(pwd)/utils"

# Verify installation
python -c "from services.basic_service import BasicServiceImpl; print('OK')"
```

### Getting Help

If you're still having issues:
1. Check our **[Development Guide](development.md)** for detailed troubleshooting
2. Review the **[Testing Guide](testing.md)** for test-specific issues
3. Look at the **[Examples](examples.md)** for working code samples

Ready to dive deeper? Our **[Testing Guide](testing.md)** shows you everything that's tested and how to run specific test scenarios! 🎉
