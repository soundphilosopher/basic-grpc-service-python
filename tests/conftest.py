"""
🔧 Pytest Configuration for BasicService Tests

This configuration file provides common fixtures and setup for testing
the BasicService gRPC implementation. It includes utilities for mocking
gRPC contexts and handling async test scenarios.
"""

import pytest
import asyncio
from unittest.mock import AsyncMock
import grpc
from grpc import aio as grpc_aio


@pytest.fixture
def event_loop():
    """
    🔄 Create an event loop for async tests.

    This fixture ensures that each test gets a fresh event loop,
    which is important for async testing to avoid state pollution
    between tests.
    """
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_grpc_context():
    """
    🎭 Create a mock gRPC service context.

    This fixture provides a properly mocked gRPC ServicerContext
    that can be used in tests without needing a real gRPC server.

    Returns:
        AsyncMock: A mock gRPC context with common methods stubbed
    """
    context = AsyncMock(spec=grpc_aio.ServicerContext)

    # Set up common context behaviors
    context.is_cancelled.return_value = False
    context.time_remaining.return_value = 30.0  # 30 seconds remaining
    context.peer.return_value = "test_client"

    return context


@pytest.fixture
def basic_service():
    """
    🏭 Create a BasicService instance for testing.

    This fixture provides a fresh BasicService instance for each test,
    ensuring test isolation and consistent starting conditions.

    Returns:
        BasicServiceImpl: A fresh service instance
    """
    from services.basic_service import BasicServiceImpl
    return BasicServiceImpl()


# Configure pytest for async testing
pytest_plugins = ('pytest_asyncio',)

# Async test configuration
@pytest.fixture(scope="session")
def asyncio_event_loop_policy():
    """Set the event loop policy for async tests."""
    return asyncio.DefaultEventLoopPolicy()
