"""
🎪 Basic Service Implementation - Where gRPC Magic Happens!

This module contains the main business logic for the BasicService, implementing
a delightfully interactive gRPC service that can:

- Greet you like a friendly neighbor 👋
- Chat with you using an AI therapist (Eliza) 🧠
- Run background tasks like a multitasking wizard ⚡

The service demonstrates various gRPC patterns including unary calls, streaming,
and background task orchestration with proper error handling and CloudEvents.

Author: The gRPC Service Squad 🦸‍♀️🦸‍♂️
"""

import asyncio
import datetime as dt
import uuid
import grpc
import logging
import random

from google.protobuf.timestamp import Timestamp
from google.protobuf.any import Any
from utils import Eliza, Some

# Generated modules (paths may differ based on your buf out dir)
from basic.v1 import basic_pb2_grpc, basic_pb2
from basic.service.v1 import service_pb2
from cloudevents.v1.cloudevents_pb2 import CloudEvent


class BasicServiceImpl(basic_pb2_grpc.BasicServiceServicer):
    """
    🌟 The star of the show - BasicService implementation!

    This class implements the BasicService gRPC interface, providing three main
    functionalities wrapped in CloudEvents for that extra enterprise sparkle ✨:

    1. Hello - A simple greeting service that says hello back
    2. Talk - A streaming chat service powered by the Eliza chatbot
    3. Background - Parallel task execution with real-time progress streaming

    Each method demonstrates different gRPC patterns:

    - Unary RPC (Hello)
    - Bidirectional streaming (Talk)
    - Server streaming with background tasks (Background)
    """

    async def Hello(self, request: service_pb2.HelloRequest, context: grpc.aio.ServicerContext) -> service_pb2.HelloResponse:
        """
        👋 Say hello in the most elaborate way possible!

        Takes a simple message and wraps it in a CloudEvent because even
        greetings deserve enterprise-grade packaging. This demonstrates
        the basic unary RPC pattern with CloudEvents integration.

        Args:
            request (service_pb2.HelloRequest): The incoming hello request with a message
            context (grpc.aio.ServicerContext): gRPC service context (standard gRPC magic)

        Returns:
            service_pb2.HelloResponse: A CloudEvent-wrapped greeting response

        Example:
            Input: HelloRequest(message="World")
            Output: HelloResponse containing CloudEvent with "Hello, World"

        Note:
            Each response gets a unique UUID and timestamp because we're fancy like that! 💅
        """
        # Create the actual greeting event payload
        event = service_pb2.HelloResponseEvent(
            greeting=f"Hello, {request.message}"
        )

        # Pack it into a protobuf Any message (because flexibility is key)
        any_payload = Any()
        any_payload.Pack(event)

        # Create a timestamp for when this magical moment happened
        timestamp = Timestamp()
        timestamp.FromDatetime(dt.datetime.now(dt.timezone.utc))

        # Wrap everything in a fancy CloudEvent envelope 📧
        cloudevent = CloudEvent(
            id=str(uuid.uuid4()),  # Every event is special and unique
            spec_version="v1.0",
            source="basic.v1.BasicService/Hello",
            type=service_pb2.DESCRIPTOR.message_types_by_name['HelloResponse'].full_name,
            attributes={
                "time": CloudEvent.CloudEventAttributeValue(ce_timestamp=timestamp),
            },
            proto_data=any_payload,
        )

        return service_pb2.HelloResponse(cloud_event=cloudevent)

    #     async def Talk(self, request_iterator: AsyncIterator[service_pb2.TalkRequest], context: grpc.aio.ServicerContext) -> AsyncIterator[service_pb2.TalkResponse]:


    async def Talk(self, request_iterator, context: grpc.aio.ServicerContext):
        """
        🧠 Have a therapeutic chat with our resident AI psychologist!

        This streaming method connects you with Eliza, the classic chatbot
        therapist. Send messages and receive thoughtful (or seemingly thoughtful)
        responses in real-time. It's like having a conversation with a very
        patient, if somewhat repetitive, therapist.

        Args:
            request_iterator: Async iterator of TalkRequest messages from the client
            context (grpc.aio.ServicerContext): gRPC service context for streaming magic

        Yields:
            service_pb2.TalkResponse: Streaming responses from our AI therapist

        Features:
            - Bidirectional streaming (talk and listen simultaneously)
            - Built-in Eliza chatbot for therapeutic conversations
            - Debug logging for conversation tracking
            - Handles client disconnection gracefully

        Example Conversation:
            Client: "I feel sad today"
            Eliza: "I am sorry to hear that you are sad."
            Client: "Why do I feel this way?"
            Eliza: "Why do you say that?"

        Note:
            Eliza might seem repetitive, but that's part of her charm! She's been
            doing this since 1966, so she's got experience. 👵
        """
        # Create our therapeutic AI companion
        eliza = Eliza()

        # Process each incoming message from the client
        async for message_request in request_iterator:
            # Get Eliza's wise response
            eliza_reply = eliza.reply(message_request.message)

            # Log the conversation for debugging (and entertainment)
            logging.debug("Talk in=%r -> out=%r goodbye=%s",
                         message_request.message, eliza_reply.text, eliza_reply.goodbye)

            # Stream back the response
            yield service_pb2.TalkResponse(answer=eliza_reply.text)

    async def Background(self, request: service_pb2.BackgroundRequest, context: grpc.aio.ServicerContext):
        """
        ⚡ The multitasking maestro - run multiple background tasks in parallel!

        This method demonstrates advanced async patterns by spinning up multiple
        background workers that simulate calling various services. It provides
        real-time progress updates via server streaming and handles errors gracefully.

        Perfect for demonstrating:

        - Parallel task execution with asyncio
        - Server-side streaming with progress updates
        - Error handling and recovery in distributed systems
        - Task cancellation on client disconnect

        Args:
            request (service_pb2.BackgroundRequest): Configuration for background tasks
            context (grpc.aio.ServicerContext): gRPC context for streaming responses

        Yields:
            service_pb2.BackgroundResponse: Stream of progress updates wrapped in CloudEvents

        Request Parameters:
            - processes (int): Number of parallel workers to spawn (defaults to 1)

        Streaming Behavior:
            1. Initial STATE_PROCESS response with empty results
            2. Updated STATE_PROCESS responses after each task completion
            3. Final STATE_COMPLETE response with all results

        Error Handling:
            - Individual task failures are captured and included as error responses
            - Client cancellation properly stops all background workers
            - Transport errors cancel all tasks and propagate the error

        Example:
            Request: BackgroundRequest(processes=3)
            Stream: [Initial empty, Progress 1/3, Progress 2/3, Progress 3/3, Final complete]

        Note:
            Workers simulate calling random services (REST, gRPC, etc.) with realistic delays.
            It's like having a team of very dedicated, if imaginary, service callers! 🏃‍♀️🏃‍♂️
        """
        # Create our service simulation helper
        some = Some()

        # Ensure we have at least one process (because zero workers accomplish nothing)
        process_count = request.processes or 1
        if process_count <= 0:
            process_count = 1

        # Record when this epic background operation began
        started_at = dt.datetime.now(dt.timezone.utc)

        # Queue for collecting worker results as they complete
        result_queue: asyncio.Queue = asyncio.Queue()
        worker_tasks = []

        async def background_worker(worker_id: int):
            """
            🔧 Individual background worker that simulates service calls.

            Each worker pretends to call a random service type (REST, gRPC, etc.)
            and takes a realistic amount of time to complete. Results are queued
            for the main streaming loop to process.

            Args:
                worker_id (int): Unique identifier for this worker

            Note:
                Uses asyncio.to_thread() to run the blocking fake_service_response
                in a thread pool, keeping our async event loop happy! 😊
            """
            try:
                # Pick a random protocol because variety is the spice of life
                protocol = random.choice([
                    "rest", "grpc", "rpc", "ws", "mqtt", "amqp",
                    "graphql", "sql", "file"
                ])

                # Simulate the service call (runs in thread to avoid blocking)
                service_result = await asyncio.to_thread(
                    some.fake_service_response,
                    f"service-{worker_id}",
                    protocol=protocol
                )

                # Deliver the good news
                await result_queue.put(service_result)

            except Exception as error:
                # Even workers have bad days - log and queue the error
                logging.exception("Background worker %s failed", worker_id)
                await result_queue.put(error)

        # Launch all our hardworking background processes
        for worker_num in range(1, process_count + 1):
            task = asyncio.create_task(background_worker(worker_num))
            worker_tasks.append(task)

        # Start the streaming show!
        try:
            # Send initial status: "We've started, but nothing's done yet"
            yield some.build_background_response(
                state=service_pb2.State.STATE_PROCESS,
                started_at=started_at,
                completed_at=None,
                responses=[]
            )

            # Track completion progress
            remaining_tasks = process_count
            completed_responses = []

            # Process results as workers complete their tasks
            while remaining_tasks > 0:
                # Wait for the next worker to finish (or fail)
                completed_item = await result_queue.get()

                if isinstance(completed_item, Exception):
                    # Handle worker failures gracefully by creating error responses
                    error_response = service_pb2.SomeServiceResponse(
                        id=str(uuid.uuid4()),
                        name="background-error",
                        version="v1",
                        data=service_pb2.SomeServiceData(
                            value=str(completed_item),
                            type="error",
                        ),
                    )
                    completed_responses.append(error_response)
                else:
                    # Success! Add the real response
                    completed_responses.append(completed_item)

                remaining_tasks -= 1

                # Send progress update with current results
                yield some.build_background_response(
                    state=service_pb2.State.STATE_PROCESS,
                    started_at=started_at,
                    completed_at=None,
                    responses=list(completed_responses)  # Send a snapshot
                )

            # Wait for all tasks to fully complete (cleanup)
            await asyncio.gather(*worker_tasks, return_exceptions=True)

            # Send final completion status with all results
            yield some.build_background_response(
                state=service_pb2.State.STATE_COMPLETE,
                started_at=started_at,
                completed_at=dt.datetime.now(dt.timezone.utc),
                responses=completed_responses
            )

        except asyncio.CancelledError:
            # Client said "never mind" - clean up our workers
            logging.info("Background operation cancelled by client")
            for task in worker_tasks:
                task.cancel()
            raise

        except grpc.aio.AioRpcError as rpc_error:
            # Network or transport issues - abort everything
            for task in worker_tasks:
                task.cancel()
            logging.warning("Background stream aborted: %s (%s)",
                          rpc_error.code(), rpc_error.details())
            raise

        except Exception:
            # Any other unexpected error - cancel tasks and re-raise
            for task in worker_tasks:
                task.cancel()
            logging.exception("Background stream encountered unexpected error")
            raise
