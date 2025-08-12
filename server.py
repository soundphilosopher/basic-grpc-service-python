import asyncio
import signal
import datetime as dt
import uuid

import grpc
from grpc_reflection.v1alpha import reflection
from google.protobuf.timestamp import Timestamp
from google.protobuf.any import Any

# Generated modules (paths may differ based on your buf out dir)
from basic.v1 import basic_pb2_grpc, basic_pb2
from basic.service.v1 import service_pb2
from cloudevents.v1.cloudevents_pb2 import CloudEvent

class BasicServiceImpl(basic_pb2_grpc.BasicServiceServicer):
    async def Hello(self, request: service_pb2.HelloRequest, context: grpc.aio.ServicerContext):
        event = service_pb2.HelloResponseEvent(
            greeting = f"Hello, {request.message}"
        )

        any = Any()
        any.Pack(event)

        ts = Timestamp()
        ts.FromDatetime(dt.datetime.now(dt.timezone.utc))

        cloudevent = CloudEvent(
            id=str(uuid.uuid4()),
            spec_version="v1.0",
            source="basic.v1.BasicService/Hello",
            type=service_pb2.DESCRIPTOR.message_types_by_name['HelloResponse'].full_name,
            attributes={
                "time": CloudEvent.CloudEventAttributeValue(ce_timestamp=ts),
            },
            proto_data=any,
        )

        return service_pb2.HelloResponse(
            cloud_event=cloudevent
        )

    async def Talk(self, request_iterator, context: grpc.aio.ServicerContext):
        # Client-streaming: consume all messages, reply once
        messages = []
        async for msg in request_iterator:
            messages.append(msg.message)
        return service_pb2.TalkResponse(answer=f"Got {len(messages)} messages")

    async def Background(self, request: service_pb2.BackgroundRequest, context: grpc.aio.ServicerContext):
        # Server-streaming: emit periodic updates
        processes = request.processes or 1

        start = Timestamp()
        start.FromDatetime(dt.datetime.now(dt.timezone.utc))

        for i in range(processes):
            # Build a BackgroundResponse with a CloudEvent if desired
            # evt = ce_pb2.CloudEvent(id=str(i), source="basic", type="BackgroundResponseEvent", ...)
            yield service_pb2.BackgroundResponse(
                # cloud_event=evt
            )
            await asyncio.sleep(0.2)

        # final “complete” event:
        # yield svc_pb2.BackgroundResponse(cloud_event=final_evt)

async def serve() -> None:
    # TLS credentials (as you already have)
    with open("certs/local.crt", "rb") as f:
        cert = f.read()
    with open("certs/local.key", "rb") as f:
        key = f.read()

    server_creds = grpc.ssl_server_credentials(
        private_key_certificate_chain_pairs=[(key, cert)],
        root_certificates=None,
        require_client_auth=False,
    )

    server = grpc.aio.server()
    basic_pb2_grpc.add_BasicServiceServicer_to_server(BasicServiceImpl(), server)

    # add reflection
    reflection.enable_server_reflection([basic_pb2.DESCRIPTOR.services_by_name['BasicService'].full_name], server)

    server.add_secure_port("127.0.0.1:8443", server_creds)

    await server.start()
    print("gRPC server listening on https://127.0.0.1:8443 (HTTP/2)")

    # ---- graceful shutdown wiring ----
    stop_event = asyncio.Event()
    loop = asyncio.get_running_loop()

    def _signal_handler():
        # Idempotent: set() can be called multiple times
        stop_event.set()

    # Try to handle POSIX signals (Linux/macOS)
    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, _signal_handler)
        except NotImplementedError:
            # Windows or environments without signal support for event loops
            pass

    # Also: if someone calls server.stop(...) elsewhere, this returns.
    # Otherwise we wait until a signal triggers the event.
    await stop_event.wait()

    print("Shutting down gracefully... (waiting up to 10s for in-flight RPCs)")
    # grace=N means: stop accepting new RPCs, allow up to N seconds for
    # existing RPCs/streams to complete before forcefully cancelling.
    await server.stop(grace=10.0)
    print("Shutdown complete.")

if __name__ == "__main__":
    asyncio.run(serve())
