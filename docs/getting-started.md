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
```

This will install all required dependencies including gRPC, protobuf, and logging libraries.

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

Now that you have the service running:

- 📖 Explore the [API Reference](reference/) to understand all available methods
- 💬 Try the [Talk service](reference/services.basic_service.md#talk) for real-time chat
- 🏃‍♂️ Test the [Background service](reference/services.basic_service.md#background) for parallel processing
- 🧠 Learn about the [Eliza chatbot](reference/utils.eliza.md) implementation

Ready to dive deeper? Check out our [Examples](examples.md) page for more advanced usage patterns!
