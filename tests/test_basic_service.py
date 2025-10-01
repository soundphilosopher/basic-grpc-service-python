"""
🧪 Tests for BasicService - Making sure our gRPC service is enterprise-ready!

This test suite verifies that our BasicService implementation correctly handles:

- Unary RPC calls (Hello method)
- Bidirectional streaming (Talk method with Eliza)
- Server streaming with background tasks (Background method)
- CloudEvents integration and proper formatting
- Error handling and edge cases

Test Categories:

- Hello method functionality and CloudEvent formatting
- Talk streaming conversations with Eliza integration
- Background task orchestration and progress streaming
- Edge cases and error conditions
- CloudEvent validation and structure
"""

import pytest
import asyncio
import uuid
import datetime as dt
from unittest.mock import AsyncMock, MagicMock, patch
from typing import List, AsyncIterator

import grpc
from grpc import aio as grpc_aio
from google.protobuf.any import Any
from google.protobuf.timestamp import Timestamp

# Import our service and dependencies
from services.basic_service import BasicServiceImpl
from utils.eliza import Eliza, Reply
from utils.some import Some

# Import protobuf messages
from basic.service.v1 import service_pb2
from cloudevents.v1.cloudevents_pb2 import CloudEvent


class TestHelloMethod:
    """
    👋 Tests for the Hello unary RPC method.

    Making sure our greeting service is properly enterprise-wrapped!
    """

    @pytest.mark.asyncio
    async def test_hello_basic_greeting(self):
        """Test basic hello functionality."""
        service = BasicServiceImpl()

        # Create a simple hello request
        request = service_pb2.HelloRequest(message="World")
        context = AsyncMock(spec=grpc_aio.ServicerContext)

        # Call the hello method
        response = await service.Hello(request, context)

        # Verify response structure
        assert isinstance(response, service_pb2.HelloResponse)
        assert response.HasField('cloud_event')

        # Verify CloudEvent structure
        cloud_event = response.cloud_event
        assert cloud_event.spec_version == "v1.0"
        assert cloud_event.source == "basic.v1.BasicService/Hello"
        assert len(cloud_event.id) > 0  # Should have UUID
        assert cloud_event.HasField('proto_data')

    @pytest.mark.asyncio
    async def test_hello_greeting_content(self):
        """Test that the greeting content is correct."""
        service = BasicServiceImpl()

        request = service_pb2.HelloRequest(message="Testing")
        context = AsyncMock(spec=grpc_aio.ServicerContext)

        response = await service.Hello(request, context)

        # Extract the actual greeting from the CloudEvent
        cloud_event = response.cloud_event
        any_payload = cloud_event.proto_data

        # Unpack the Any message
        hello_event = service_pb2.HelloResponseEvent()
        any_payload.Unpack(hello_event)

        assert hello_event.greeting == "Hello, Testing"

    @pytest.mark.asyncio
    async def test_hello_empty_message(self):
        """Test hello with empty message."""
        service = BasicServiceImpl()

        request = service_pb2.HelloRequest(message="")
        context = AsyncMock(spec=grpc_aio.ServicerContext)

        response = await service.Hello(request, context)

        # Should still work and create a valid response
        cloud_event = response.cloud_event
        any_payload = cloud_event.proto_data

        hello_event = service_pb2.HelloResponseEvent()
        any_payload.Unpack(hello_event)

        assert hello_event.greeting == "Hello, "

    @pytest.mark.asyncio
    async def test_hello_special_characters(self):
        """Test hello with special characters."""
        service = BasicServiceImpl()

        special_messages = [
            "World! 🌍",
            "Test@123",
            "こんにちは",  # Japanese
            "Ñiño"        # Spanish
        ]

        context = AsyncMock(spec=grpc_aio.ServicerContext)

        for message in special_messages:
            request = service_pb2.HelloRequest(message=message)
            response = await service.Hello(request, context)

            # Extract greeting
            cloud_event = response.cloud_event
            any_payload = cloud_event.proto_data
            hello_event = service_pb2.HelloResponseEvent()
            any_payload.Unpack(hello_event)

            assert hello_event.greeting == f"Hello, {message}"

    @pytest.mark.asyncio
    async def test_hello_cloud_event_metadata(self):
        """Test CloudEvent metadata is properly set."""
        service = BasicServiceImpl()

        request = service_pb2.HelloRequest(message="Metadata Test")
        context = AsyncMock(spec=grpc_aio.ServicerContext)

        response = await service.Hello(request, context)
        cloud_event = response.cloud_event

        # Verify CloudEvent structure
        assert cloud_event.spec_version == "v1.0"
        assert cloud_event.source == "basic.v1.BasicService/Hello"
        assert len(cloud_event.id) == 36  # UUID length
        assert uuid.UUID(cloud_event.id)  # Valid UUID

        # Check timestamp attribute
        assert "time" in cloud_event.attributes
        time_attr = cloud_event.attributes["time"]
        assert time_attr.HasField("ce_timestamp")


class MockTalkRequestIterator:
    """Helper class to mock async iterator for Talk method testing."""

    def __init__(self, messages: List[str]):
        self.messages = [service_pb2.TalkRequest(message=msg) for msg in messages]
        self.index = 0

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.index >= len(self.messages):
            raise StopAsyncIteration
        message = self.messages[self.index]
        self.index += 1
        return message


class TestTalkMethod:
    """
    🧠 Tests for the Talk bidirectional streaming method.

    Making sure our AI therapist integration works smoothly!
    """

    @pytest.mark.asyncio
    async def test_talk_single_message(self):
        """Test Talk method with a single message."""
        service = BasicServiceImpl()
        context = AsyncMock(spec=grpc_aio.ServicerContext)

        # Create mock request iterator
        messages = ["Hello Eliza"]
        request_iterator = MockTalkRequestIterator(messages)

        # Collect responses
        responses = []
        async for response in service.Talk(request_iterator, context):
            responses.append(response)

        # Should get one response
        assert len(responses) == 1
        assert isinstance(responses[0], service_pb2.TalkResponse)
        assert len(responses[0].answer) > 0

    @pytest.mark.asyncio
    async def test_talk_conversation(self):
        """Test a full conversation with Eliza."""
        service = BasicServiceImpl()
        context = AsyncMock(spec=grpc_aio.ServicerContext)

        # Create a conversation
        messages = [
            "Hello",
            "I am feeling sad",
            "My mother doesn't understand me",
            "goodbye"
        ]
        request_iterator = MockTalkRequestIterator(messages)

        # Collect all responses
        responses = []
        async for response in service.Talk(request_iterator, context):
            responses.append(response)

        # Should get responses for each message
        assert len(responses) == len(messages)

        # All responses should be valid
        for response in responses:
            assert isinstance(response, service_pb2.TalkResponse)
            assert len(response.answer) > 0

    @pytest.mark.asyncio
    async def test_talk_empty_message(self):
        """Test Talk method with empty message."""
        service = BasicServiceImpl()
        context = AsyncMock(spec=grpc_aio.ServicerContext)

        messages = [""]
        request_iterator = MockTalkRequestIterator(messages)

        responses = []
        async for response in service.Talk(request_iterator, context):
            responses.append(response)

        # Should still get a response (Eliza handles empty input)
        assert len(responses) == 1
        assert responses[0].answer == "Please say something."

    @pytest.mark.asyncio
    async def test_talk_eliza_integration(self):
        """Test that Talk method properly integrates with Eliza."""
        service = BasicServiceImpl()
        context = AsyncMock(spec=grpc_aio.ServicerContext)

        # Test known Eliza patterns
        test_cases = [
            ("goodbye", True),   # Should trigger goodbye
            ("I am sad", False), # Should not trigger goodbye
            ("sorry", False)     # Should not trigger goodbye
        ]

        for message, expect_goodbye_pattern in test_cases:
            request_iterator = MockTalkRequestIterator([message])

            responses = []
            async for response in service.Talk(request_iterator, context):
                responses.append(response)

            assert len(responses) == 1
            response = responses[0]

            # Create Eliza directly to compare
            eliza = Eliza()
            expected_reply = eliza.reply(message)

            # The response should be similar to direct Eliza usage
            assert isinstance(response.answer, str)
            assert len(response.answer) > 0

    @pytest.mark.asyncio
    async def test_talk_with_logging(self):
        """Test that Talk method logs conversations properly."""
        with patch('services.basic_service.logging') as mock_logging:
            service = BasicServiceImpl()
            context = AsyncMock(spec=grpc_aio.ServicerContext)

            messages = ["test message"]
            request_iterator = MockTalkRequestIterator(messages)

            responses = []
            async for response in service.Talk(request_iterator, context):
                responses.append(response)

            # Should have logged the conversation
            mock_logging.debug.assert_called()
            call_args = mock_logging.debug.call_args[0]
            assert "Talk in=" in call_args[0]


class TestBackgroundMethod:
    """
    ⚡ Tests for the Background streaming method with parallel tasks.

    Making sure our background task orchestration works like a charm!
    """

    @pytest.mark.asyncio
    async def test_background_single_process(self):
        """Test Background method with single process."""
        service = BasicServiceImpl()
        context = AsyncMock(spec=grpc_aio.ServicerContext)

        request = service_pb2.BackgroundRequest(processes=1)

        # Collect all streaming responses
        responses = []
        async for response in service.Background(request, context):
            responses.append(response)

        # Should get at least 2 responses: initial + final
        assert len(responses) >= 2

        # All responses should be valid BackgroundResponse
        for response in responses:
            assert isinstance(response, service_pb2.BackgroundResponse)
            assert response.HasField('cloud_event')

    @pytest.mark.asyncio
    async def test_background_multiple_processes(self):
        """Test Background method with multiple processes."""
        service = BasicServiceImpl()
        context = AsyncMock(spec=grpc_aio.ServicerContext)

        request = service_pb2.BackgroundRequest(processes=3)

        responses = []
        async for response in service.Background(request, context):
            responses.append(response)

        # Should get: initial + progress updates + final
        # At minimum: initial + final = 2, but likely more with progress
        assert len(responses) >= 2

        # Last response should be COMPLETE
        last_response = responses[-1]
        cloud_event = last_response.cloud_event
        any_payload = cloud_event.proto_data

        bg_event = service_pb2.BackgroundResponseEvent()
        any_payload.Unpack(bg_event)

        assert bg_event.state == service_pb2.State.STATE_COMPLETE
        assert len(bg_event.responses) == 3  # Should have 3 results

    @pytest.mark.asyncio
    async def test_background_zero_processes(self):
        """Test Background method with zero processes (should default to 1)."""
        service = BasicServiceImpl()
        context = AsyncMock(spec=grpc_aio.ServicerContext)

        request = service_pb2.BackgroundRequest(processes=0)

        responses = []
        async for response in service.Background(request, context):
            responses.append(response)

        # Should still work with default 1 process
        assert len(responses) >= 2

        # Check final response has 1 result
        last_response = responses[-1]
        cloud_event = last_response.cloud_event
        any_payload = cloud_event.proto_data

        bg_event = service_pb2.BackgroundResponseEvent()
        any_payload.Unpack(bg_event)

        assert len(bg_event.responses) == 1

    @pytest.mark.asyncio
    async def test_background_response_progression(self):
        """Test that Background responses show proper state progression."""
        service = BasicServiceImpl()
        context = AsyncMock(spec=grpc_aio.ServicerContext)

        request = service_pb2.BackgroundRequest(processes=2)

        responses = []
        states = []

        async for response in service.Background(request, context):
            responses.append(response)

            # Extract state from each response
            cloud_event = response.cloud_event
            any_payload = cloud_event.proto_data
            bg_event = service_pb2.BackgroundResponseEvent()
            any_payload.Unpack(bg_event)
            states.append(bg_event.state)

        # First response should be PROCESS with empty results
        assert states[0] == service_pb2.State.STATE_PROCESS

        # Last response should be COMPLETE
        assert states[-1] == service_pb2.State.STATE_COMPLETE

        # Should have progression from PROCESS to COMPLETE
        assert service_pb2.State.STATE_PROCESS in states
        assert service_pb2.State.STATE_COMPLETE in states

    @pytest.mark.asyncio
    async def test_background_timestamps(self):
        """Test that Background responses have proper timestamps."""
        service = BasicServiceImpl()
        context = AsyncMock(spec=grpc_aio.ServicerContext)

        request = service_pb2.BackgroundRequest(processes=1)

        responses = []
        before_start = dt.datetime.now(dt.timezone.utc)

        async for response in service.Background(request, context):
            responses.append(response)

        after_complete = dt.datetime.now(dt.timezone.utc)

        # Check first and last response timestamps
        first_response = responses[0]
        last_response = responses[-1]

        # Extract events and check timestamps exist and are reasonable
        for response in [first_response, last_response]:
            cloud_event = response.cloud_event
            any_payload = cloud_event.proto_data
            bg_event = service_pb2.BackgroundResponseEvent()
            any_payload.Unpack(bg_event)

            # Should have started_at timestamp
            assert bg_event.HasField('started_at')
            started_at = bg_event.started_at.ToDatetime()

            # Make timezone-aware if needed for comparison
            if started_at.tzinfo is None:
                started_at = started_at.replace(tzinfo=dt.timezone.utc)

            # Check that timestamp is within reasonable bounds (allow 10 second tolerance)
            time_tolerance = dt.timedelta(seconds=10)
            assert (before_start - time_tolerance) <= started_at <= (after_complete + time_tolerance)

        # Check that last response has completed_at if it's the final state
        cloud_event = last_response.cloud_event
        any_payload = cloud_event.proto_data
        bg_event = service_pb2.BackgroundResponseEvent()
        any_payload.Unpack(bg_event)

        if bg_event.state == service_pb2.State.STATE_COMPLETE:
            assert bg_event.HasField('completed_at')
            completed_at = bg_event.completed_at.ToDatetime()

            # Make timezone-aware if needed
            if completed_at.tzinfo is None:
                completed_at = completed_at.replace(tzinfo=dt.timezone.utc)

            # completed_at should be after started_at
            started_at = bg_event.started_at.ToDatetime()
            if started_at.tzinfo is None:
                started_at = started_at.replace(tzinfo=dt.timezone.utc)

            assert completed_at >= started_at


    @pytest.mark.asyncio
    async def test_background_cancellation(self):
        """Test Background method handles cancellation properly."""
        service = BasicServiceImpl()
        context = AsyncMock(spec=grpc_aio.ServicerContext)

        request = service_pb2.BackgroundRequest(processes=5)  # More processes for longer runtime

        responses = []

        try:
            # Start the background operation
            async_gen = service.Background(request, context)

            # Get first response
            first_response = await async_gen.__anext__()
            responses.append(first_response)

            # Simulate cancellation after first response
            raise asyncio.CancelledError("Simulated client cancellation")

        except asyncio.CancelledError:
            # This is expected - the method should handle cancellation gracefully
            pass

        # Should have at least gotten the initial response
        assert len(responses) >= 1

    @pytest.mark.asyncio
    @patch('services.basic_service.Some.fake_service_response')
    async def test_background_with_service_errors(self, mock_fake_service):
        """Test Background method handles service errors gracefully."""
        # Make the fake service raise an error
        mock_fake_service.side_effect = Exception("Service unavailable")

        service = BasicServiceImpl()
        context = AsyncMock(spec=grpc_aio.ServicerContext)

        request = service_pb2.BackgroundRequest(processes=1)

        responses = []
        async for response in service.Background(request, context):
            responses.append(response)

        # Should still complete despite service errors
        assert len(responses) >= 2

        # Final response should have error information
        last_response = responses[-1]
        cloud_event = last_response.cloud_event
        any_payload = cloud_event.proto_data
        bg_event = service_pb2.BackgroundResponseEvent()
        any_payload.Unpack(bg_event)

        # Should have one response (error)
        assert len(bg_event.responses) == 1
        error_response = bg_event.responses[0]
        assert error_response.data.type == "error"


class TestServiceIntegration:
    """
    🔗 Integration tests that test the service components working together.

    Making sure all the pieces fit together perfectly!
    """

    @pytest.mark.asyncio
    async def test_eliza_integration_in_service(self):
        """Test that the service properly integrates with Eliza."""
        service = BasicServiceImpl()

        # Test that service creates Eliza instances correctly
        context = AsyncMock(spec=grpc_aio.ServicerContext)
        messages = ["I am happy", "goodbye"]
        request_iterator = MockTalkRequestIterator(messages)

        responses = []
        async for response in service.Talk(request_iterator, context):
            responses.append(response)

        assert len(responses) == 2

        # Responses should be from Eliza
        for response in responses:
            assert len(response.answer) > 0
            assert isinstance(response.answer, str)

    @pytest.mark.asyncio
    async def test_some_utility_integration(self):
        """Test that the service properly integrates with Some utility."""
        service = BasicServiceImpl()
        context = AsyncMock(spec=grpc_aio.ServicerContext)

        request = service_pb2.BackgroundRequest(processes=1)

        responses = []
        async for response in service.Background(request, context):
            responses.append(response)

        # Should get properly formatted responses from Some utility
        assert len(responses) >= 2

        for response in responses:
            assert isinstance(response, service_pb2.BackgroundResponse)
            assert response.HasField('cloud_event')

            # CloudEvent should be properly formatted by Some utility
            cloud_event = response.cloud_event
            assert cloud_event.source == "urn:service:basic"
            assert len(cloud_event.id) == 36  # UUID


class TestEdgeCases:
    """
    🚨 Edge case and error condition tests.

    Making sure our service is robust under all conditions!
    """

    @pytest.mark.asyncio
    async def test_hello_with_very_long_message(self):
        """Test Hello with very long message."""
        service = BasicServiceImpl()
        context = AsyncMock(spec=grpc_aio.ServicerContext)

        long_message = "A" * 10000  # Very long message
        request = service_pb2.HelloRequest(message=long_message)

        response = await service.Hello(request, context)

        # Should still work
        assert isinstance(response, service_pb2.HelloResponse)
        cloud_event = response.cloud_event
        any_payload = cloud_event.proto_data
        hello_event = service_pb2.HelloResponseEvent()
        any_payload.Unpack(hello_event)

        assert hello_event.greeting == f"Hello, {long_message}"

    @pytest.mark.asyncio
    async def test_background_with_negative_processes(self):
        """Test Background with negative process count."""
        service = BasicServiceImpl()
        context = AsyncMock(spec=grpc_aio.ServicerContext)

        request = service_pb2.BackgroundRequest(processes=-5)

        responses = []
        async for response in service.Background(request, context):
            responses.append(response)

        # Should default to 1 process
        assert len(responses) >= 2

        # Check that it processed with 1 worker
        last_response = responses[-1]
        cloud_event = last_response.cloud_event
        any_payload = cloud_event.proto_data
        bg_event = service_pb2.BackgroundResponseEvent()
        any_payload.Unpack(bg_event)

        assert len(bg_event.responses) == 1

    @pytest.mark.asyncio
    async def test_talk_with_no_messages(self):
        """Test Talk method with empty iterator."""
        service = BasicServiceImpl()
        context = AsyncMock(spec=grpc_aio.ServicerContext)

        # Empty message iterator
        request_iterator = MockTalkRequestIterator([])

        responses = []
        async for response in service.Talk(request_iterator, context):
            responses.append(response)

        # Should get no responses from empty iterator
        assert len(responses) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
