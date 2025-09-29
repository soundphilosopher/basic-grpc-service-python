# 🚀 Basic gRPC Service in Python

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![gRPC](https://img.shields.io/badge/gRPC-1.74+-green.svg?style=flat-square&logo=grpc&logoColor=white)](https://grpc.io/)
[![ConnectRPC](https://img.shields.io/badge/ConnectRPC-0.4.2-purple.svg?style=flat-square)](https://connectrpc.com/)
[![Buf](https://img.shields.io/badge/Buf-v2-orange.svg?style=flat-square&logo=buf&logoColor=white)](https://buf.build/)
[![MkDocs](https://img.shields.io/badge/Docs-MkDocs-blue.svg?style=flat-square&logo=readthedocs&logoColor=white)](https://soundphilosopher.github.io/basic-grpc-service-python/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)

> A delightfully modern gRPC service showcasing async Python, streaming, cloud events, and comprehensive documentation! 🎉

## ✨ What's This All About?

This is a **production-ready gRPC service** that demonstrates modern Python gRPC development with:

- 🔄 **Bidirectional streaming** - Talk to our chatbot in real-time
- ⚡ **Async/await** everywhere for maximum performance
- 🎭 **Background task orchestration** with live progress updates
- ☁️ **CloudEvents** integration for event-driven architecture
- 🔐 **TLS/SSL** with self-signed certificates
- 🏥 **Health checks** and **reflection** built-in
- 📊 **Structured JSON logging** for observability
- 🏗️ **Modular architecture** with clean separation of concerns
- 📚 **Comprehensive documentation** with MkDocs and GitHub Pages

## 🛠️ The Tech Stack

This project uses some seriously cool technology:

| Technology | Purpose | Why It's Awesome |
|------------|---------|------------------|
| **[ConnectRPC](https://connectrpc.com/)** | gRPC Framework | Modern, type-safe, and works everywhere |
| **[Buf](https://buf.build/)** | Protobuf Management | No more protoc headaches! |
| **[MkDocs](https://mkdocs.org/)** | Documentation | Beautiful docs with GitHub Pages |
| **[mkcert](https://github.com/FiloSottile/mkcert)** | Local TLS Certs | Trusted certificates in seconds |
| **[protoc-gen-init_python](https://pypi.org/project/protobuf-init/)** | Python Package Structure | Automatically creates `__init__.py` files |
| **[CloudEvents](https://cloudevents.io/)** | Event Standardization | Industry standard for event data |

## 🚦 Quick Start

### Prerequisites

- **Python 3.10+** (because we're living in the future! 🚀)
- **mkcert** for generating local certificates
- **buf CLI** (optional, for proto management)

### 1. 🔧 Generate Local Certificates

First, let's get some shiny certificates:

```bash
# Install mkcert (if you haven't already)
# On macOS: brew install mkcert
# On Windows: choco install mkcert
# On Linux: check your package manager

# Install the local CA
mkcert -install

# Generate certificates for localhost
mkcert -cert-file ./certs/local.crt -key-file ./certs/local.key localhost 127.0.0.1 0.0.0.0 ::1
```

### 2. 📦 Install Dependencies

```bash
# Install the project in development mode
python -m pip install -e .

# Or install with development dependencies
python -m pip install -e ".[dev]"

# Or install with documentation dependencies
python -m pip install -e ".[docs]"
```

### 3. 🎬 Start the Server

```bash
python server.py
```

You should see something like:
```json
{"level": "INFO", "message": "gRPC server listening on https://127.0.0.1:8443 (HTTP/2)", "time": "2024-01-01T12:00:00.000Z"}
```

## 📚 Documentation

This project includes comprehensive documentation built with **MkDocs** and deployed to **GitHub Pages**.

### 🌐 Online Documentation

Visit our beautiful documentation site: **[https://soundphilosopher.github.io/basic-grpc-service-python/](https://soundphilosopher.github.io/basic-grpc-service-python/)**

### 🏠 Local Documentation

To build and serve the documentation locally:

```bash
# Quick setup and serve (recommended)
./scripts/setup_docs.sh

# Manual setup
pip install -e ".[docs]"
mkdocs serve
```

The documentation will be available at `http://127.0.0.1:8000`

### 📖 Documentation Features

- **API Reference**: Auto-generated from docstrings
- **Getting Started Guide**: Step-by-step setup instructions
- **Examples**: Code examples for all service methods
- **Development Guide**: Contributing and development workflows
- **Beautiful Theme**: Material Design with dark/light mode toggle

## 🎮 Let's Play!

### Method 1: Using grpcurl (Recommended)

Install [grpcurl](https://github.com/fullstorydev/grpcurl) and start exploring:

```bash
# 🔍 Discover available services
grpcurl 127.0.0.1:8443 list

# 🔍 List methods of BasicService
grpcurl 127.0.0.1:8443 list basic.v1.BasicService

# 👋 Say hello (unary RPC)
grpcurl -d '{"message": "World"}' 127.0.0.1:8443 basic.v1.BasicService/Hello

# 💬 Have a conversation (bidirectional streaming)
cat <<EOF | grpcurl -d @ 127.0.0.1:8443 basic.v1.BasicService/Talk
{"message": "Hello there!"}
{"message": "How are you doing?"}
{"message": "What's your favorite color?"}
{"message": "Goodbye!"}
EOF

# 🏃‍♂️ Run background tasks (server streaming)
grpcurl -d '{"processes": 3}' 127.0.0.1:8443 basic.v1.BasicService/Background
```

### Method 2: Using Python Client

Create a simple client script:

```python
import asyncio
import grpc
from basic.v1 import basic_pb2_grpc
from basic.service.v1 import service_pb2

async def main():
    # Create insecure channel for testing
    async with grpc.aio.insecure_channel('127.0.0.1:8443') as channel:
        stub = basic_pb2_grpc.BasicServiceStub(channel)

        # Say hello
        response = await stub.Hello(service_pb2.HelloRequest(message="Python"))
        print(f"Server says: {response}")

if __name__ == "__main__":
    asyncio.run(main())
```

## 🏗️ Project Structure

```
basic-grpc-service-python/
├── 📁 proto/                    # Protocol Buffers definitions
│   ├── basic/v1/basic.proto     # Service definitions
│   └── basic/service/v1/        # Message types
├── 📁 sdk/                      # Generated Python code
│   └── basic/                   # Auto-generated from protos
├── 📁 services/                 # 🆕 Modular service implementations
│   ├── __init__.py              # Service package initialization
│   └── basic_service.py         # BasicService implementation
├── 📁 utils/                    # Utility modules
│   ├── eliza.py                 # ELIZA chatbot implementation
│   └── some.py                  # CloudEvents and helper functions
├── 📁 docs/                     # 🆕 MkDocs documentation source
│   ├── index.md                 # Documentation homepage
│   ├── getting-started.md       # Setup and installation guide
│   ├── examples.md              # Code examples and usage
│   └── development.md           # Development and contributing guide
├── 📁 scripts/                  # 🆕 Automation scripts
│   ├── setup_docs.sh            # Build and serve docs locally
│   ├── deploy_pages.sh          # Deploy docs to GitHub Pages
│   └── gen_ref_pages.py         # Generate API reference pages
├── 📁 certs/                    # TLS certificates
│   ├── local.crt               # Certificate file
│   └── local.key               # Private key
├── 📁 site/                     # 🆕 Built documentation (auto-generated)
├── 🐍 server.py                 # Main server implementation
├── 📋 pyproject.toml            # Python project configuration
├── 📚 mkdocs.yml                # 🆕 MkDocs configuration
├── 🛡️ buf.yaml                  # Buf configuration
├── ⚙️ buf.gen.yaml              # Code generation config
└── 📄 LICENSE                   # MIT License
```

## 🎯 Service Methods

### 👋 `Hello` - Simple Unary RPC
Send a greeting and get a CloudEvent-wrapped response back.

**Request:** `HelloRequest`
```protobuf
message HelloRequest {
  string message = 1;
}
```

**Response:** `HelloResponse` (wrapped in CloudEvent)
```protobuf
message HelloResponse {
  cloudevents.v1.CloudEvent cloud_event = 1;
}
```

### 💬 `Talk` - Bidirectional Streaming
Have a conversation with our simple chatbot. Send messages and get responses in real-time!

**Stream:** `TalkRequest` ⇄ `TalkResponse`

### 🏃‍♂️ `Background` - Server Streaming
Kick off multiple background tasks and watch their progress in real-time. Perfect for demonstrating long-running operations!

**Request:** `BackgroundRequest`
```protobuf
message BackgroundRequest {
  int32 processes = 1; // Number of background workers
}
```

**Stream Response:** Live updates as tasks complete!

## 🔧 Development

### 🏗️ Modular Architecture

The service has been refactored into a clean, modular architecture:

- **`services/`**: Contains all gRPC service implementations
- **`utils/`**: Reusable utility functions and classes
- **`server.py`**: Main server orchestration and startup

This makes the codebase easier to maintain, test, and extend.

### 📝 Documentation Workflow

We use **MkDocs** with **Material theme** for our documentation:

```bash
# Setup and serve docs locally
./scripts/setup_docs.sh

# Deploy to GitHub Pages
./scripts/deploy_pages.sh

# Generate API reference pages
python scripts/gen_ref_pages.py
```

### Regenerating Code

If you modify the `.proto` files, regenerate the Python code:

```bash
buf generate
```

### Code Generation Features

- **ConnectRPC Python**: Modern async gRPC client/server code
- **Standard gRPC**: Traditional gRPC bindings
- **Type Stubs**: Full typing support with `.pyi` files
- **Auto __init__.py**: Automatically creates package structure

### Health Checks

The server includes gRPC health checking:

```bash
# Check overall server health
grpcurl -insecure 127.0.0.1:8443 grpc.health.v1.Health/Check

# Check specific service health
grpcurl -insecure -d '{"service":"basic.v1.BasicService"}' 127.0.0.1:8443 grpc.health.v1.Health/Check
```

## 🚀 Features

- ✅ **Modular architecture** with clean separation of concerns
- ✅ **Comprehensive documentation** with MkDocs and GitHub Pages
- ✅ **Automated documentation deployment** with GitHub Actions
- ✅ **API reference generation** from docstrings
- ✅ **Development and documentation dependencies** in pyproject.toml
- ✅ **Helper scripts** for common development tasks
- ✅ **Async/await** throughout for non-blocking I/O
- ✅ **TLS encryption** with self-signed certificates
- ✅ **Graceful shutdown** handling (SIGINT/SIGTERM)
- ✅ **Structured JSON logging** for observability
- ✅ **Health checks** and service reflection
- ✅ **CloudEvents** integration for event-driven patterns
- ✅ **Streaming RPCs** for real-time communication
- ✅ **Background task orchestration** with progress updates
- ✅ **Type safety** with protobuf and Python type hints

## 🐛 Troubleshooting

### Certificate Issues
If you get certificate errors:
```bash
# Recreate certificates
rm certs/local.*
mkcert -cert-file ./certs/local.crt -key-file ./certs/local.key localhost 127.0.0.1
```

### Port Already in Use
```bash
# Kill any process using port 8443
lsof -ti:8443 | xargs kill -9
```

### Import Errors
Make sure you've installed the project:
```bash
python -m pip install -e .
```

### Documentation Issues
If documentation doesn't build:
```bash
# Clean and rebuild
rm -rf site/
pip install -e ".[docs]"
mkdocs build
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Found a bug or have an improvement? Pull requests are welcome! This is a learning project, so let's learn together. 🎓

Check out our [Development Guide](https://soundphilosopher.github.io/basic-grpc-service-python/development/) for detailed contributing instructions.

## 🎉 Credits

Built with ❤️ using:
- [gRPC](https://grpc.io/) for the communication protocol
- [ConnectRPC](https://connectrpc.com/) for modern gRPC tooling
- [Buf](https://buf.build/) for painless protobuf management
- [MkDocs](https://mkdocs.org/) and [Material theme](https://squidfunk.github.io/mkdocs-material/) for beautiful documentation
- [CloudEvents](https://cloudevents.io/) for standardized event data
- [mkcert](https://github.com/FiloSottile/mkcert) for hassle-free local HTTPS

---

*Happy gRPC-ing! 🚀
