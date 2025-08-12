import asyncio
import signal
import datetime as dt
import uuid
import threading
import grpc
import logging
import random

from time import sleep
from concurrent import futures
from grpc_reflection.v1alpha import reflection
from grpc_health.v1 import health_pb2_grpc, health, health_pb2
from google.protobuf.timestamp import Timestamp
from google.protobuf.any import Any
from pythonjsonlogger.json import JsonFormatter
from utils import Utils

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

    async def Talk(self, request_iterator, context):
        talk = Utils.Talk()

        async for msg in request_iterator:
            result = talk.reply(msg.message)
            logging.debug("Talk in=%r -> out=%r goodbye=%s",
                            msg.message, result.text, result.goodbye)

            yield service_pb2.TalkResponse(answer=result.text)

    async def Background(self, request: service_pb2.BackgroundRequest, context: grpc.aio.ServicerContext):
        some = Utils.Some()

        count = request.processes or 1
        if count <= 0:
            count = 1

        started_at_dt = dt.datetime.now(dt.timezone.utc)

        async def _to_ts(dtobj: dt.datetime) -> Timestamp:
            ts = Timestamp()
            ts.FromDatetime(dtobj)
            return ts

        # Fan-out: kick off N background workers
        queue: asyncio.Queue = asyncio.Queue()
        tasks = []

        async def worker(pid: int):
            try:
                protocol = random.choice(["rest", "grpc", "rpc", "ws", "mqtt", "amqp", "graphql", "sql", "file"])
                # fake_service_response() blocks (uses time.sleep), so run it in a thread:
                result = await asyncio.to_thread(some.fake_service_response, f"service-{pid}", protocol=protocol)
                await queue.put(result)
            except Exception as e:
                logging.exception("Background worker %s failed", pid)
                await queue.put(e)

        for i in range(1, count + 1):
            tasks.append(asyncio.create_task(worker(i)))

        # Stream: initial empty snapshot (PROCESS state)
        try:
            yield some.build_background_response(
                state=service_pb2.State.STATE_PROCESS,
                started_at=started_at_dt,
                completed_at=None,
                responses=[]
            )

            remaining = count
            responses = []

            while remaining > 0:
                item = await queue.get()

                if isinstance(item, Exception):
                    # Surface errors as synthetic response entries (and still make progress)
                    responses.append(
                        service_pb2.SomeServiceResponse(
                            id=str(uuid.uuid4()),
                            name="background-error",
                            version="v1",
                            data=service_pb2.SomeServiceData(
                                value=str(item),
                                type="error",
                            ),
                        )
                    )
                    remaining -= 1
                else:
                    responses.append(item)
                    remaining -= 1

                # Stream updated snapshot after each completion
                yield some.build_background_response(
                    state=service_pb2.State.STATE_PROCESS,
                    started_at=started_at_dt,
                    completed_at=None,
                    responses=list(responses)  # copy snapshot
                )

            # All workers done → final COMPLETE with full set
            await asyncio.gather(*tasks, return_exceptions=True)

            yield some.build_background_response(
                state=service_pb2.State.STATE_COMPLETE,
                started_at=started_at_dt,
                completed_at=dt.datetime.now(dt.timezone.utc),
                responses=responses
            )

        except asyncio.CancelledError:
            # Client cancelled or stream torn down; stop workers
            for t in tasks:
                t.cancel()
            raise
        except grpc.aio.AioRpcError as e:
            # Stream error from transport; stop workers
            for t in tasks:
                t.cancel()
            logging.warning("Background stream aborted: %s (%s)", e.code(), e.details())
            raise
        except Exception:
            # Any other server error; stop workers
            for t in tasks:
                t.cancel()
            logging.exception("Background stream error")
            raise

def _toggle_health(health_servicer: health.HealthServicer, service: str):
    next_status = health_pb2.HealthCheckResponse.SERVING
    while True:
        if next_status == health_pb2.HealthCheckResponse.SERVING:
            next_status = health_pb2.HealthCheckResponse.NOT_SERVING
        else:
            next_status = health_pb2.HealthCheckResponse.SERVING

        health_servicer.set(service, next_status)
        logging.debug(
            f"Health status for '{service}' set to "
            f"{health_pb2.HealthCheckResponse.ServingStatus.Name(next_status)}"
        )

        sleep(5)

def _configure_health_server(server: grpc.aio.Server):
    health_servicer = health.HealthServicer(
        experimental_non_blocking=True,
        experimental_thread_pool=futures.ThreadPoolExecutor(max_workers=10),
    )
    health_pb2_grpc.add_HealthServicer_to_server(health_servicer, server)

    # Use a daemon thread to toggle health status
    toggle_health_status_thread = threading.Thread(
        target=_toggle_health,
        args=(health_servicer, basic_pb2.DESCRIPTOR.services_by_name['BasicService'].full_name),
        daemon=True,
    )
    toggle_health_status_thread.start()

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

    # add health check
    _configure_health_server(server)

    server.add_secure_port("127.0.0.1:8443", server_creds)

    await server.start()
    logging.info("gRPC server listening on https://127.0.0.1:8443 (HTTP/2)")

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

    logging.info("Shutting down gracefully... (waiting up to 10s for in-flight RPCs)")
    # grace=N means: stop accepting new RPCs, allow up to N seconds for
    # existing RPCs/streams to complete before forcefully cancelling.
    await server.stop(grace=10.0)
    logging.info("Shutdown complete.")

if __name__ == "__main__":
    json_log_handler = logging.StreamHandler()
    formatter = JsonFormatter(
        "{levelname}{message}{asctime}",
        style="{",
        rename_fields={"levelname": "level", "asctime": "time"}
    )
    json_log_handler.setFormatter(formatter)

    logging.basicConfig(level=logging.DEBUG, handlers=[json_log_handler])

    asyncio.run(serve())
