# 🧪 Testing Guide

This project includes a comprehensive test suite with over **80 test cases** covering all functionality from unit tests to integration scenarios. Our testing approach ensures reliability, maintainability, and confidence in deployments.

## 📊 Test Coverage Overview

| Component | Test File | Coverage | Test Count |
|-----------|-----------|----------|------------|
| **Eliza Chatbot** | `test_eliza.py` | 90%+ | 40+ tests |
| **BasicService** | `test_basic_service.py` | 95%+ | 40+ tests |
| **Integration** | Built into service tests | 85%+ | Embedded |

### 🎯 What's Tested

- ✅ **Pattern Matching** - All conversation patterns and edge cases
- ✅ **gRPC Methods** - Hello, Talk, and Background with full scenarios
- ✅ **Streaming** - Bidirectional and server streaming with proper async handling
- ✅ **CloudEvents** - Proper event structure and metadata validation
- ✅ **Error Handling** - Cancellation, timeouts, and service failures
- ✅ **Edge Cases** - Empty inputs, special characters, very long messages

## 🚀 Quick Start Testing

### Run All Tests (Recommended)

```bash
# Complete test suite with pretty output
./scripts/run_tests.sh

# With coverage reporting
./scripts/run_tests.sh --coverage

# Verbose debugging output
./scripts/run_tests.sh --verbose
```

### Fast Development Testing

```bash
# Skip dependency checks (faster repeated runs)
./scripts/run_tests.sh --fast

# Run specific test file
python -m pytest tests/test_eliza.py -v

# Run specific test method
python -m pytest tests/test_basic_service.py::TestHelloMethod::test_hello_basic_greeting -v
```

## 🔧 Test Runner Features

Our enhanced test runner (`scripts/run_tests.sh`) provides:

- **🎨 Color-coded output** for better readability
- **📊 Coverage reporting** with HTML and terminal views
- **🔍 Automatic test discovery** and file listing
- **🚨 Smart error handling** with debugging tips
- **⚙️ Multiple modes** (fast, verbose, coverage)
- **✨ Professional output** with progress indicators

### Command Line Options

```bash
./scripts/run_tests.sh [OPTIONS]

Options:
  --coverage    Generate and display coverage reports
  --verbose     Maximum verbosity for debugging
  --fast        Skip dependency installation (faster)
  --help        Show detailed usage information
```

## 🧠 Eliza Chatbot Tests

Our Eliza implementation has extensive test coverage:

### Pattern Matching Tests

```python
def test_apology_handling_simple():
    """Test responses to simple apology."""
    eliza = Eliza()
    reply = eliza.reply("sorry")
    assert len(reply.text) > 0
    assert not reply.goodbye
```

### Conversation Flow Tests

```python
def test_basic_conversation():
    """Test a complete conversation flow."""
    eliza = Eliza()

    # Multi-turn conversation
    responses = [
        eliza.reply("Hello"),
        eliza.reply("I feel sad"),
        eliza.reply("goodbye")
    ]

    # Verify conversation progression
    assert len(responses) == 3
    assert responses[-1].goodbye  # Should detect goodbye
```

### Edge Case Testing

- **Empty inputs** → "Please say something."
- **Special characters** → Handled gracefully
- **Very long messages** → Processed without errors
- **Mixed case inputs** → Normalized properly

## ⚡ gRPC Service Tests

Comprehensive testing of all service methods:

### Hello Method Tests

```python
@pytest.mark.asyncio
async def test_hello_basic_greeting():
    """Test basic hello functionality."""
    service = BasicServiceImpl()
    context = AsyncMock(spec=grpc_aio.ServicerContext)

    request = service_pb2.HelloRequest(message="World")
    response = await service.Hello(request, context)

    # Verify CloudEvent structure
    assert isinstance(response, service_pb2.HelloResponse)
    assert response.HasField('cloud_event')
    assert len(response.cloud_event.id) == 36  # UUID length
```

### Talk Method Tests (Streaming)

```python
@pytest.mark.asyncio
async def test_talk_conversation():
    """Test bidirectional streaming conversation."""
    service = BasicServiceImpl()
    context = AsyncMock(spec=grpc_aio.ServicerContext)

    messages = ["Hello", "I am sad", "goodbye"]
    request_iterator = MockTalkRequestIterator(messages)

    responses = []
    async for response in service.Talk(request_iterator, context):
        responses.append(response)

    assert len(responses) == len(messages)
    # All responses should be valid TalkResponse objects
    for response in responses:
        assert isinstance(response, service_pb2.TalkResponse)
        assert len(response.answer) > 0
```

### Background Method Tests (Server Streaming)

```python
@pytest.mark.asyncio
async def test_background_multiple_processes():
    """Test background processing with multiple workers."""
    service = BasicServiceImpl()
    context = AsyncMock(spec=grpc_aio.ServicerContext)

    request = service_pb2.BackgroundRequest(processes=3)

    responses = []
    async for response in service.Background(request, context):
        responses.append(response)

    # Should get: initial + progress updates + final
    assert len(responses) >= 2

    # Final response should be COMPLETE with 3 results
    last_response = responses[-1]
    # ... verification of response structure
```

## 📊 Coverage Reports

### Generate Coverage Reports

```bash
# Run tests with coverage
./scripts/run_tests.sh --coverage

# View HTML report
python -m http.server 8000 -d htmlcov/
# Then open: http://localhost:8000
```

### Coverage Targets

We maintain high coverage standards:

- **Services** (`services/`) → **95%+** coverage
- **Utils** (`utils/`) → **90%+** coverage
- **Overall project** → **90%+** coverage

### Reading Coverage Reports

The HTML coverage report shows:

- **Green lines** → Covered by tests ✅
- **Red lines** → Not covered ❌
- **Yellow lines** → Partially covered ⚠️

## 🐛 Debugging Failed Tests

### Common Test Failures

#### 1. **Import Errors**

```bash
# Fix: Ensure proper installation
python -m pip install -e ".[dev]"

# Verify Python path
export PYTHONPATH="$PYTHONPATH:$(pwd):$(pwd)/sdk"
```

#### 2. **Async Test Issues**

```bash
# Fix: Use proper asyncio mode
python -m pytest tests/ --asyncio-mode=auto

# Or run specific async test
python -m pytest tests/test_basic_service.py::TestBackgroundMethod -v --asyncio-mode=auto
```

#### 3. **Timezone/DateTime Errors**

```bash
# Run specific failing test with max verbosity
python -m pytest tests/test_basic_service.py::TestBackgroundMethod::test_background_timestamps -vvv -s
```

### Advanced Debugging

```bash
# Run with Python debugger
python -m pytest tests/test_eliza.py --pdb

# Maximum verbosity with no output capture
python -m pytest tests/ -vvv -s --tb=long

# Run single test with detailed output
./scripts/run_tests.sh --verbose
```

## 🎯 Test Configuration

### pytest Configuration (`pyproject.toml`)

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "-v --tb=short"
```

### Test Fixtures (`tests/conftest.py`)

```python
@pytest.fixture
def mock_grpc_context():
    """Create a mock gRPC service context."""
    context = AsyncMock(spec=grpc_aio.ServicerContext)
    context.is_cancelled.return_value = False
    return context

@pytest.fixture
def basic_service():
    """Create a BasicService instance for testing."""
    return BasicServiceImpl()
```

## ✅ Best Practices

### Writing New Tests

1. **Use descriptive names**: `test_hello_with_empty_message_returns_valid_response`
2. **Test behavior, not implementation**: Focus on what the code should do
3. **Include edge cases**: Empty inputs, special characters, error conditions
4. **Use proper async patterns**: `@pytest.mark.asyncio` for async tests
5. **Mock external dependencies**: Use `AsyncMock` for gRPC contexts

### Test Structure

```python
# tests/test_your_feature.py
import pytest
from unittest.mock import AsyncMock

class TestYourFeature:
    """Test suite for YourFeature functionality."""

    def test_basic_functionality(self):
        """Test basic feature operation."""
        # Arrange
        # Act
        # Assert

    @pytest.mark.asyncio
    async def test_async_functionality(self):
        """Test async feature operation."""
        # Arrange
        service = BasicServiceImpl()
        context = AsyncMock(spec=grpc_aio.ServicerContext)

        # Act
        result = await service.method(request, context)

        # Assert
        assert result is not None
```

### Continuous Integration

Tests should pass before merging:

```bash
# Pre-commit testing checklist
./scripts/run_tests.sh --coverage  # All tests pass ✅
# Coverage above 90% ✅
# No flaky tests ✅
# Documentation updated ✅
```

## 🎉 Test Results

When all tests pass, you'll see:

```bash
🎉 All tests passed!

📊 Coverage report generated:
  📄 Terminal summary: shown above
  📊 HTML report: htmlcov/index.html

💡 To view the HTML coverage report:
  python -m http.server 8000 -d htmlcov/
  Then open: http://localhost:8000

✅ Test suite completed successfully!
Your gRPC service is ready for production! 🚀
```

Ready to test? Run `./scripts/run_tests.sh --coverage` and see the magic! ✨
