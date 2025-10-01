"""
🚀 Basic gRPC Service Server

A delightfully secure and robust gRPC server implementation that serves your basic service
with TLS encryption, health checks, and graceful shutdown capabilities. Because who doesn't
love a server that knows how to say goodbye properly? 👋

This module provides the main server entry point for the Basic gRPC service, complete with:

- SSL/TLS security (because security is not optional!)
- Health checking (to keep your service feeling great)
- Server reflection (for introspection and debugging)
- Graceful shutdown handling (because abrupt endings are for bad movies)

Example:
    Run the server directly from the command line:

    ```shell
    $ python server.py

    The server will start listening on https://127.0.0.1:8443 with JSON logging.
    ```

Author: The gRPC Wizards ✨
"""

import asyncio
import signal
import grpc
import logging

from concurrent import futures
from grpc_reflection.v1alpha import reflection
from grpc_health.v1 import health_pb2_grpc, health, health_pb2
from pythonjsonlogger.json import JsonFormatter
from services import BasicServiceImpl

# Generated modules (paths may differ based on your buf out dir)
from basic.v1 import basic_pb2_grpc, basic_pb2


async def serve() -> None:
    """
    🎪 The main circus tent where all the gRPC magic happens!

    Spins up a fully-featured gRPC server with all the bells and whistles:

    - TLS encryption using local certificates
    - Service implementation registration
    - Health check endpoint (because health matters!)
    - Server reflection for easy debugging
    - Graceful shutdown handling (the polite way to exit)

    The server listens on 127.0.0.1:8443 and uses HTTP/2 for that modern touch.
    When shutdown signals are received (SIGINT, SIGTERM), the server gracefully
    stops accepting new requests and allows existing ones up to 10 seconds to complete.

    Raises:
        FileNotFoundError: If the TLS certificate files are missing from certs/
        grpc.RpcError: If there are issues starting the gRPC server

    Note:
        Make sure you have valid TLS certificates in the certs/ directory:

        - certs/local.crt (certificate file)
        - certs/local.key (private key file)
    """
    # Load TLS credentials like a boss 🔐
    # (Because plain HTTP is so 1990s)
    with open("certs/local.crt", "rb") as f:
        cert = f.read()
    with open("certs/local.key", "rb") as f:
        key = f.read()

    server_creds = grpc.ssl_server_credentials(
        private_key_certificate_chain_pairs=[(key, cert)],
        root_certificates=None,
        require_client_auth=False,  # We're friendly, no client certs required
    )

    # Create our shiny new server instance
    server = grpc.aio.server()

    # Register our basic service implementation
    # (This is where the actual business logic lives!)
    basic_pb2_grpc.add_BasicServiceServicer_to_server(BasicServiceImpl(), server)

    # Enable reflection for debugging and introspection
    # (Because sometimes you need to look in the mirror)
    reflection.enable_server_reflection([
        basic_pb2.DESCRIPTOR.services_by_name['BasicService'].full_name
    ], server)

    # Set up health checking service
    # (Keep your service healthy, just like eating your vegetables 🥕)
    health_servicer = health.HealthServicer(
        experimental_non_blocking=True,
        experimental_thread_pool=futures.ThreadPoolExecutor(max_workers=10),
    )

    # Set health status for the overall server and specific service
    health_servicer.set("", health_pb2.HealthCheckResponse.UNKNOWN)
    health_servicer.set(
        basic_pb2.DESCRIPTOR.services_by_name['BasicService'].full_name,
        health_pb2.HealthCheckResponse.SERVING
    )

    health_pb2_grpc.add_HealthServicer_to_server(health_servicer, server)

    # Bind to our local address with TLS
    server.add_secure_port("127.0.0.1:8443", server_creds)

    # 🚀 Launch sequence initiated!
    await server.start()
    logging.info("gRPC server listening on https://127.0.0.1:8443 (HTTP/2)")

    # ---- Graceful shutdown orchestration ----
    # (Because good servers know how to make a graceful exit)
    stop_event = asyncio.Event()
    loop = asyncio.get_running_loop()

    def _signal_handler() -> None:
        """
        🛑 The polite way to ask the server to stop.

        This signal handler sets the stop event, which triggers the graceful
        shutdown sequence. It's idempotent, so multiple signals won't cause issues.
        Think of it as the server's "please wrap up what you're doing" bell.
        """
        stop_event.set()

    # Register signal handlers for graceful shutdown
    # (SIGINT = Ctrl+C, SIGTERM = polite termination request)
    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, _signal_handler)
        except NotImplementedError:
            # Windows or environments that don't support signal handling in event loops
            # (Windows, you're special, but not in a bad way... mostly)
            pass

    # Wait for the stop signal like a patient butler
    await stop_event.wait()

    logging.info("Shutting down gracefully... (waiting up to 10s for in-flight RPCs)")

    # Grace period: Stop accepting new requests, allow existing ones to complete
    # (10 seconds should be enough for most polite RPCs to finish their business)
    await server.stop(grace=10.0)
    logging.info("Shutdown complete. Thanks for using our service! 👋")


if __name__ == "__main__":
    """
    🎬 The main event! Set up logging and start the server.

    Configures JSON logging for structured output (because logs should be
    machine-readable AND human-friendly) and then runs the main server
    coroutine.
    """
    # Set up fancy JSON logging (because plain text logs are for cavemen)
    json_log_handler = logging.StreamHandler()
    formatter = JsonFormatter(
        "{levelname}{message}{asctime}",
        style="{",
        rename_fields={"levelname": "level", "asctime": "time"}
    )
    json_log_handler.setFormatter(formatter)

    # Configure logging with DEBUG level for maximum visibility
    logging.basicConfig(level=logging.DEBUG, handlers=[json_log_handler])

    # 🎭 And... action! Start the async event loop and serve
    asyncio.run(serve())
