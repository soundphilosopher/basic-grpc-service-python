"""
🛠️ Some Utility - The Swiss Army Knife of gRPC Services

This module provides utility functions for building CloudEvent responses
and simulating service calls. Think of it as the helpful assistant that
handles all the boring but necessary stuff so your main service can focus
on being awesome! ⚡

Key Features:
- CloudEvent response building with proper formatting
- Service call simulation with realistic delays
- Timestamp conversion utilities for protobuf integration
- Background task orchestration support

The name "Some" might seem mysterious, but sometimes you just need "some"
utility functions to get the job done! 🔧

Author: The Utility Squad 🦸‍♀️🦸‍♂️
"""

import random
import uuid
import time as _time
import datetime as dt

from dataclasses import dataclass
from typing import List, Tuple, Optional, Pattern

from google.protobuf.any import Any
from google.protobuf.timestamp import Timestamp
from cloudevents.v1.cloudevents_pb2 import CloudEvent
from basic.service.v1 import service_pb2


class Some:
    """
    🎭 The master of ceremonies for background operations and service simulation!

    This utility class provides essential functions for:
    - Building properly formatted CloudEvent responses
    - Simulating realistic service calls with delays
    - Converting between datetime formats and protobuf timestamps
    - Supporting the Background streaming service with progress updates

    Why "Some"? Because sometimes you need some help, and this class
    provides some very useful functions! It's like having a reliable
    friend who always knows how to format timestamps correctly. 👯‍♀️
    """

    def build_background_response(self, *, state: service_pb2.State, started_at: dt.datetime, completed_at: Optional[dt.datetime], responses: List[service_pb2.SomeServiceResponse]) -> service_pb2.BackgroundResponse:
        """
        🏗️ Construct a beautifully wrapped CloudEvent response for background operations.

        This method is the master builder for BackgroundResponse messages. It takes
        your raw response data and wraps it in a proper CloudEvent envelope with
        all the metadata bells and whistles. Because even background responses
        deserve to look professional! ✨

        Args:
            state: The current state of the background operation (PROCESS/COMPLETE)
            started_at (datetime): When the background operation began
            completed_at (datetime, optional): When it completed (None if still running)
            responses (list): List of SomeServiceResponse messages collected so far

        Returns:
            service_pb2.BackgroundResponse: A properly formatted response with CloudEvent

        CloudEvent Details:
            - Unique UUID for each response (because every response is special)
            - Source URN identifying this service
            - CloudEvents v1.0 spec compliance
            - Timestamp metadata for event tracking
            - Protobuf payload with proper type information

        Example:
            >>> some = Some()
            >>> response = some.build_background_response(
            ...     state=service_pb2.State.STATE_PROCESS,
            ...     started_at=datetime.now(timezone.utc),
            ...     completed_at=None,
            ...     responses=[]
            ... )

        Note:
            This method uses keyword-only arguments to prevent parameter mix-ups.
            Because nobody wants to accidentally pass completed_at as state! 🤦‍♀️
        """
        # Create the actual response payload with all the juicy details
        payload_event = service_pb2.BackgroundResponseEvent(
            state=state,
            started_at=self._to_ts(started_at),
            completed_at=self._to_ts(completed_at) if completed_at else None,
            responses=responses,  # All the hard-earned results from our workers
        )

        # Pack the payload into a protobuf Any message for maximum flexibility
        any_message = Any()
        any_message.Pack(payload_event)  # This sets the type_url automagically

        # Create a timestamp for this exact moment in space-time
        current_timestamp = self._to_ts(dt.datetime.now(dt.timezone.utc))

        # Wrap everything in a fancy CloudEvent envelope 📨
        cloud_event = CloudEvent(
            id=str(uuid.uuid4()),  # Every event deserves its own unique identity
            source="urn:service:basic",  # Where this event came from
            spec_version="1.0",  # We follow the standards like good citizens
            type=payload_event.DESCRIPTOR.full_name,  # Full protobuf message name
            attributes={
                "time": CloudEvent.CloudEventAttributeValue(ce_timestamp=current_timestamp),
            },
            proto_data=any_message,  # The actual payload, safely packaged
        )

        return service_pb2.BackgroundResponse(cloud_event=cloud_event)

    def fake_service_response(self, service_name: str, protocol: str) -> service_pb2.SomeServiceResponse:
        """
        🎪 Simulate a realistic service call with all the drama of real networking!

        This method pretends to call an external service by sleeping for a random
        duration (because real services are unpredictable) and then returns a
        properly formatted response. It's like method acting for microservices! 🎭

        Perfect for:
        - Testing background processing patterns
        - Demonstrating concurrent service calls
        - Creating realistic delays in development
        - Impressing your colleagues with your attention to detail

        Args:
            service_name (str): Name of the service being "called" (e.g., "user-service")
            protocol (str): Protocol type (rest, grpc, mqtt, etc.)

        Returns:
            service_pb2.SomeServiceResponse: A realistic-looking service response

        Timing:
            Random delay between 1-3 seconds (because real services are moody)

        Response Format:
            - Unique UUID for tracking
            - Service name and version info
            - Protocol data wrapped in SomeServiceData

        Example:
            >>> some = Some()
            >>> response = some.fake_service_response("auth-service", "grpc")
            >>> response.name
            "auth-service"
            >>> response.data.type
            "protocol"

        Note:
            This method uses time.sleep() which blocks the thread! That's why
            the Background service calls it with asyncio.to_thread() to avoid
            blocking the event loop. Safety first! 🛡️
        """
        # Simulate realistic network delay (1-3 seconds of "networking")
        _time.sleep(random.uniform(1.0, 3.0))

        # Create a realistic service response with all the proper fields
        return service_pb2.SomeServiceResponse(
            id=str(uuid.uuid4()),  # Every response gets its own tracking ID
            name=service_name,     # The service we "called"
            version="v1",          # Always version your services, kids!
            data=service_pb2.SomeServiceData(
                value=str(protocol),  # What protocol we "used"
                type="protocol",      # Metadata about the data type
            ),
        )

    def _to_ts(self, when: dt.datetime|int|float) -> Timestamp:
        """
        ⏰ The time wizard - convert any time format to protobuf Timestamp!

        This utility method handles the annoying task of converting between
        Python datetime objects (and epoch seconds) to protobuf Timestamps.
        It's like a universal translator for time formats! 🌍

        Handles multiple input formats:
        - datetime objects (timezone-aware preferred)
        - Unix epoch seconds (int or float)
        - Automatically converts to UTC if needed

        Args:
            time_input: The time value to convert
                - datetime: Python datetime object
                - int/float: Unix epoch seconds
                - None: Returns None (for convenience)

        Returns:
            Timestamp: A properly formatted protobuf Timestamp

        Raises:
            TypeError: If the input type is not supported

        Examples:
            >>> some = Some()
            >>> now = datetime.now(timezone.utc)
            >>> ts = some._to_ts(now)
            >>> isinstance(ts, Timestamp)
            True

            >>> epoch_ts = some._to_ts(1640995200.0)  # Unix epoch
            >>> epoch_ts.seconds
            1640995200

        Time Zone Handling:
            - Naive datetime objects are assumed to be UTC
            - Timezone-aware objects are converted to UTC
            - UTC is the only truth in distributed systems! 🌐

        Note:
            The underscore prefix indicates this is a "private" method,
            but it's so useful that we document it anyway! 🤫
        """
        ts = Timestamp()
        if isinstance(when, dt.datetime):
            # Ensure timezone-aware UTC
            if when.tzinfo is None:
                when = when.replace(tzinfo=dt.timezone.utc)
            else:
                when = when.astimezone(dt.timezone.utc)
            ts.FromDatetime(when)
        elif isinstance(when, (int, float)):
            seconds = int(when)
            nanos = int((when - seconds) * 1_000_000_000)
            ts.seconds = seconds
            ts.nanos = nanos
        else:
            raise TypeError("to_ts expects a datetime or epoch seconds (int/float)")
        return ts
