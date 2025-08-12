# Generated Connect client code

from __future__ import annotations
from collections.abc import AsyncIterator
from collections.abc import Iterator
from collections.abc import Iterable
import aiohttp
import urllib3
import typing
import sys

from connectrpc.client_async import AsyncConnectClient
from connectrpc.client_sync import ConnectClient
from connectrpc.client_protocol import ConnectProtocol
from connectrpc.client_connect import ConnectProtocolError
from connectrpc.headers import HeaderInput
from connectrpc.server import ClientRequest
from connectrpc.server import ClientStream
from connectrpc.server import ServerResponse
from connectrpc.server import ServerStream
from connectrpc.server_sync import ConnectWSGI
from connectrpc.streams import StreamInput
from connectrpc.streams import AsyncStreamOutput
from connectrpc.streams import StreamOutput
from connectrpc.unary import UnaryOutput
from connectrpc.unary import ClientStreamingOutput

if typing.TYPE_CHECKING:
    # wsgiref.types was added in Python 3.11.
    if sys.version_info >= (3, 11):
        from wsgiref.types import WSGIApplication
    else:
        from _typeshed.wsgi import WSGIApplication

import basic.service.v1.service_pb2

class BasicServiceClient:
    def __init__(
        self,
        base_url: str,
        http_client: urllib3.PoolManager | None = None,
        protocol: ConnectProtocol = ConnectProtocol.CONNECT_PROTOBUF,
    ):
        self.base_url = base_url
        self._connect_client = ConnectClient(http_client, protocol)
    def call_hello(
        self, req: basic.service.v1.service_pb2.HelloRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[basic.service.v1.service_pb2.HelloResponse]:
        """Low-level method to call Hello, granting access to errors and metadata"""
        url = self.base_url + "/basic.v1.BasicService/Hello"
        return self._connect_client.call_unary(url, req, basic.service.v1.service_pb2.HelloResponse,extra_headers, timeout_seconds)


    def hello(
        self, req: basic.service.v1.service_pb2.HelloRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> basic.service.v1.service_pb2.HelloResponse:
        response = self.call_hello(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def talk(
        self, reqs: Iterable[basic.service.v1.service_pb2.TalkRequest], extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> Iterator[basic.service.v1.service_pb2.TalkResponse]:
        return self._talk_iterator(reqs, extra_headers, timeout_seconds)

    def _talk_iterator(
        self, reqs: Iterable[basic.service.v1.service_pb2.TalkRequest], extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> Iterator[basic.service.v1.service_pb2.TalkResponse]:
        stream_output = self.call_talk(reqs, extra_headers, timeout_seconds)
        err = stream_output.error()
        if err is not None:
            raise err
        yield from stream_output
        err = stream_output.error()
        if err is not None:
            raise err

    def call_talk(
        self, reqs: Iterable[basic.service.v1.service_pb2.TalkRequest], extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> StreamOutput[basic.service.v1.service_pb2.TalkResponse]:
        """Low-level method to call Talk, granting access to errors and metadata"""
        url = self.base_url + "/basic.v1.BasicService/Talk"
        return self._connect_client.call_bidirectional_streaming(
            url, reqs, basic.service.v1.service_pb2.TalkResponse, extra_headers, timeout_seconds
        )

    def background(
        self, req: basic.service.v1.service_pb2.BackgroundRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> Iterator[basic.service.v1.service_pb2.BackgroundResponse]:
        return self._background_iterator(req, extra_headers, timeout_seconds)

    def _background_iterator(
        self, req: basic.service.v1.service_pb2.BackgroundRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> Iterator[basic.service.v1.service_pb2.BackgroundResponse]:
        stream_output = self.call_background(req, extra_headers)
        err = stream_output.error()
        if err is not None:
            raise err
        yield from stream_output
        err = stream_output.error()
        if err is not None:
            raise err

    def call_background(
        self, req: basic.service.v1.service_pb2.BackgroundRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> StreamOutput[basic.service.v1.service_pb2.BackgroundResponse]:
        """Low-level method to call Background, granting access to errors and metadata"""
        url = self.base_url + "/basic.v1.BasicService/Background"
        return self._connect_client.call_server_streaming(
            url, req, basic.service.v1.service_pb2.BackgroundResponse, extra_headers, timeout_seconds
        )


class AsyncBasicServiceClient:
    def __init__(
        self,
        base_url: str,
        http_client: aiohttp.ClientSession,
        protocol: ConnectProtocol = ConnectProtocol.CONNECT_PROTOBUF,
    ):
        self.base_url = base_url
        self._connect_client = AsyncConnectClient(http_client, protocol)

    async def call_hello(
        self, req: basic.service.v1.service_pb2.HelloRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[basic.service.v1.service_pb2.HelloResponse]:
        """Low-level method to call Hello, granting access to errors and metadata"""
        url = self.base_url + "/basic.v1.BasicService/Hello"
        return await self._connect_client.call_unary(url, req, basic.service.v1.service_pb2.HelloResponse,extra_headers, timeout_seconds)

    async def hello(
        self, req: basic.service.v1.service_pb2.HelloRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> basic.service.v1.service_pb2.HelloResponse:
        response = await self.call_hello(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def talk(
        self, reqs: StreamInput[basic.service.v1.service_pb2.TalkRequest], extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> AsyncIterator[basic.service.v1.service_pb2.TalkResponse]:
        return self._talk_iterator(reqs, extra_headers, timeout_seconds)

    async def _talk_iterator(
        self, reqs: StreamInput[basic.service.v1.service_pb2.TalkRequest], extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> AsyncIterator[basic.service.v1.service_pb2.TalkResponse]:
        stream_output = await self.call_talk(reqs, extra_headers, timeout_seconds)
        err = stream_output.error()
        if err is not None:
            raise err
        async with stream_output as stream:
            async for response in stream:
                yield response
            err = stream.error()
            if err is not None:
                raise err

    async def call_talk(
        self, reqs: StreamInput[basic.service.v1.service_pb2.TalkRequest], extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> AsyncStreamOutput[basic.service.v1.service_pb2.TalkResponse]:
        """Low-level method to call Talk, granting access to errors and metadata"""
        url = self.base_url + "/basic.v1.BasicService/Talk"
        return await self._connect_client.call_bidirectional_streaming(
            url, reqs, basic.service.v1.service_pb2.TalkResponse, extra_headers, timeout_seconds
        )

    def background(
        self, req: basic.service.v1.service_pb2.BackgroundRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> AsyncIterator[basic.service.v1.service_pb2.BackgroundResponse]:
        return self._background_iterator(req, extra_headers, timeout_seconds)

    async def _background_iterator(
        self, req: basic.service.v1.service_pb2.BackgroundRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> AsyncIterator[basic.service.v1.service_pb2.BackgroundResponse]:
        stream_output = await self.call_background(req, extra_headers)
        err = stream_output.error()
        if err is not None:
            raise err
        async with stream_output as stream:
            async for response in stream:
                yield response
            err = stream.error()
            if err is not None:
                raise err

    async def call_background(
        self, req: basic.service.v1.service_pb2.BackgroundRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> AsyncStreamOutput[basic.service.v1.service_pb2.BackgroundResponse]:
        """Low-level method to call Background, granting access to errors and metadata"""
        url = self.base_url + "/basic.v1.BasicService/Background"
        return await self._connect_client.call_server_streaming(
            url, req, basic.service.v1.service_pb2.BackgroundResponse, extra_headers, timeout_seconds
        )


@typing.runtime_checkable
class BasicServiceProtocol(typing.Protocol):
    def hello(self, req: ClientRequest[basic.service.v1.service_pb2.HelloRequest]) -> ServerResponse[basic.service.v1.service_pb2.HelloResponse]:
        ...
    def talk(self, req: ClientStream[basic.service.v1.service_pb2.TalkRequest]) -> ServerStream[basic.service.v1.service_pb2.TalkResponse]:
        ...
    def background(self, req: ClientRequest[basic.service.v1.service_pb2.BackgroundRequest]) -> ServerStream[basic.service.v1.service_pb2.BackgroundResponse]:
        ...

BASIC_SERVICE_PATH_PREFIX = "/basic.v1.BasicService"

def wsgi_basic_service(implementation: BasicServiceProtocol) -> WSGIApplication:
    app = ConnectWSGI()
    app.register_unary_rpc("/basic.v1.BasicService/Hello", implementation.hello, basic.service.v1.service_pb2.HelloRequest)
    app.register_bidi_streaming_rpc("/basic.v1.BasicService/Talk", implementation.talk, basic.service.v1.service_pb2.TalkRequest)
    app.register_server_streaming_rpc("/basic.v1.BasicService/Background", implementation.background, basic.service.v1.service_pb2.BackgroundRequest)
    return app
