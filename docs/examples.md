# 🎮 Examples

Here are practical examples showing how to use the Basic gRPC Service in different scenarios.

## 🤖 Python Client Examples

### Simple Hello Client

```python
# File: examples/hello_client.py
import asyncio
import grpc
from basic.v1 import basic_pb2_grpc
from basic.service.v1 import service_pb2

async def simple_hello():
    """Simple example calling the Hello method."""
    async with grpc.aio.insecure_channel('127.0.0.1:8443') as channel:
        stub = basic_pb2_grpc.BasicServiceStub(channel)

        request = service_pb2.HelloRequest(message="MkDocs User")
        response = await stub.Hello(request)

        print(f"✅ Server responded with CloudEvent:")
        print(f"   ID: {response.cloud_event.id}")
        print(f"   Source: {response.cloud_event.source}")
        print(f"   Type: {response.cloud_event.type}")

if __name__ == "__main__":
    asyncio.run(simple_hello())
```

### Chat Client with Eliza

```python
# File: examples/chat_client.py
import asyncio
import grpc
from basic.v1 import basic_pb2_grpc
from basic.service.v1 import service_pb2

async def chat_with_eliza():
    """Interactive chat with the Eliza chatbot."""
    async with grpc.aio.insecure_channel('127.0.0.1:8443') as channel:
        stub = basic_pb2_grpc.BasicServiceStub(channel)

        # Messages to send
        messages = [
            "Hello there!",
            "I am feeling a bit sad today",
            "My mother never understood me",
            "Do you think that's normal?",
            "Goodbye"
        ]

        async def generate_requests():
            for msg in messages:
                print(f"👤 You: {msg}")
                yield service_pb2.TalkRequest(message=msg)
                await asyncio.sleep(1)  # Pause between messages

        # Start the conversation
        async for response in stub.Talk(generate_requests()):
            print(f"🧠 Eliza: {response.answer}")
            print()

if __name__ == "__main__":
    asyncio.run(chat_with_eliza())
```

### Background Tasks Client

```python
# File: examples/background_client.py
import asyncio
import grpc
from basic.v1 import basic_pb2_grpc
from basic.service.v1 import service_pb2

async def monitor_background_tasks():
    """Monitor background task execution with live updates."""
    async with grpc.aio.insecure_channel('127.0.0.1:8443') as channel:
        stub = basic_pb2_grpc.BasicServiceStub(channel)

        # Request 5 background processes
        request = service_pb2.BackgroundRequest(processes=5)

        print("🚀 Starting background tasks...")
        print("📊 Monitoring progress:\n")

        async for response in stub.Background(request):
            event = response.cloud_event

            # Extract the actual event data (this requires protobuf unpacking)
            print(f"📅 Event ID: {event.id}")
            print(f"📍 Source: {event.source}")
            print(f"⏰ Time: {event.attributes['time'].ce_timestamp}")
            print(f"📦 Responses collected: {len(response.cloud_event.proto_data)}")
            print("---")

if __name__ == "__main__":
    asyncio.run(monitor_background_tasks())
```

## 🌐 Using grpcurl (Command Line)

### Basic Service Discovery

```bash
# Discover all available services
grpcurl -insecure 127.0.0.1:8443 list

# List methods for BasicService
grpcurl -insecure 127.0.0.1:8443 list basic.v1.BasicService

# Get service description
grpcurl -insecure 127.0.0.1:8443 describe basic.v1.BasicService
```

### Hello Method Examples

```bash
# Simple hello
grpcurl -insecure -d '{"message": "World"}' \
  127.0.0.1:8443 basic.v1.BasicService/Hello

# Hello with custom message
grpcurl -insecure -d '{"message": "MkDocs Documentation"}' \
  127.0.0.1:8443 basic.v1.BasicService/Hello
```

### Talk Method Examples

```bash
# Single message chat
echo '{"message": "Hello Eliza!"}' | \
  grpcurl -insecure -d @ 127.0.0.1:8443 basic.v1.BasicService/Talk

# Multi-message conversation
cat <<EOF | grpcurl -insecure -d @ 127.0.0.1:8443 basic.v1.BasicService/Talk
{"message": "Hello there"}
{"message": "I feel anxious today"}
{"message": "What should I do?"}
{"message": "Thank you for listening"}
{"message": "Goodbye"}
EOF
```

### Background Method Examples

```bash
# Run 3 background processes
grpcurl -insecure -d '{"processes": 3}' \
  127.0.0.1:8443 basic.v1.BasicService/Background

# Run 10 background processes (stress test!)
grpcurl -insecure -d '{"processes": 10}' \
  127.0.0.1:8443 basic.v1.BasicService/Background
```

## 🏥 Health Check Examples

```bash
# Check overall server health
grpcurl -insecure 127.0.0.1:8443 grpc.health.v1.Health/Check

# Check BasicService specifically
grpcurl -insecure -d '{"service": "basic.v1.BasicService"}' \
  127.0.0.1:8443 grpc.health.v1.Health/Check

# Watch health status (streaming)
grpcurl -insecure -d '{"service": "basic.v1.BasicService"}' \
  127.0.0.1:8443 grpc.health.v1.Health/Watch
```

## 🐛 Debugging and Development

### Server Reflection Examples

```bash
# List all services (including reflection and health)
grpcurl -insecure 127.0.0.1:8443 list

# Get full service descriptor
grpcurl -insecure 127.0.0.1:8443 describe basic.v1.BasicService.Hello

# Explore message types
grpcurl -insecure 127.0.0.1:8443 describe basic.service.v1.HelloRequest
```

### Testing Error Scenarios

```bash
# Test with invalid JSON (should fail gracefully)
grpcurl -insecure -d '{"invalid": "data"}' \
  127.0.0.1:8443 basic.v1.BasicService/Hello

# Test with missing fields
grpcurl -insecure -d '{}' \
  127.0.0.1:8443 basic.v1.BasicService/Hello
```

These examples demonstrate the flexibility and power of your gRPC service! Try them out and see the beautiful responses with CloudEvents, real-time streaming, and background processing in action. 🎉
