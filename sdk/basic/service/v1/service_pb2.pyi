import datetime

from cloudevents.v1 import cloudevents_pb2 as _cloudevents_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class State(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    STATE_UNSPECIFIED: _ClassVar[State]
    STATE_PROCESS: _ClassVar[State]
    STATE_COMPLETE: _ClassVar[State]
    STATE_ERROR: _ClassVar[State]
    STATE_COMPLETE_WITH_ERROR: _ClassVar[State]
STATE_UNSPECIFIED: State
STATE_PROCESS: State
STATE_COMPLETE: State
STATE_ERROR: State
STATE_COMPLETE_WITH_ERROR: State

class SomeServiceData(_message.Message):
    __slots__ = ("value", "type")
    VALUE_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    value: str
    type: str
    def __init__(self, value: _Optional[str] = ..., type: _Optional[str] = ...) -> None: ...

class SomeServiceResponse(_message.Message):
    __slots__ = ("id", "name", "version", "data")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    version: str
    data: SomeServiceData
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., version: _Optional[str] = ..., data: _Optional[_Union[SomeServiceData, _Mapping]] = ...) -> None: ...

class SomeServiceResponses(_message.Message):
    __slots__ = ("responses",)
    RESPONSES_FIELD_NUMBER: _ClassVar[int]
    responses: _containers.RepeatedCompositeFieldContainer[SomeServiceResponse]
    def __init__(self, responses: _Optional[_Iterable[_Union[SomeServiceResponse, _Mapping]]] = ...) -> None: ...

class HelloRequest(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class HelloResponse(_message.Message):
    __slots__ = ("cloud_event",)
    CLOUD_EVENT_FIELD_NUMBER: _ClassVar[int]
    cloud_event: _cloudevents_pb2.CloudEvent
    def __init__(self, cloud_event: _Optional[_Union[_cloudevents_pb2.CloudEvent, _Mapping]] = ...) -> None: ...

class HelloResponseEvent(_message.Message):
    __slots__ = ("greeting",)
    GREETING_FIELD_NUMBER: _ClassVar[int]
    greeting: str
    def __init__(self, greeting: _Optional[str] = ...) -> None: ...

class TalkRequest(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class TalkResponse(_message.Message):
    __slots__ = ("answer",)
    ANSWER_FIELD_NUMBER: _ClassVar[int]
    answer: str
    def __init__(self, answer: _Optional[str] = ...) -> None: ...

class BackgroundRequest(_message.Message):
    __slots__ = ("processes",)
    PROCESSES_FIELD_NUMBER: _ClassVar[int]
    processes: int
    def __init__(self, processes: _Optional[int] = ...) -> None: ...

class BackgroundResponse(_message.Message):
    __slots__ = ("cloud_event",)
    CLOUD_EVENT_FIELD_NUMBER: _ClassVar[int]
    cloud_event: _cloudevents_pb2.CloudEvent
    def __init__(self, cloud_event: _Optional[_Union[_cloudevents_pb2.CloudEvent, _Mapping]] = ...) -> None: ...

class BackgroundResponseEvent(_message.Message):
    __slots__ = ("state", "started_at", "completed_at", "responses")
    STATE_FIELD_NUMBER: _ClassVar[int]
    STARTED_AT_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_AT_FIELD_NUMBER: _ClassVar[int]
    RESPONSES_FIELD_NUMBER: _ClassVar[int]
    state: State
    started_at: _timestamp_pb2.Timestamp
    completed_at: _timestamp_pb2.Timestamp
    responses: _containers.RepeatedCompositeFieldContainer[SomeServiceResponse]
    def __init__(self, state: _Optional[_Union[State, str]] = ..., started_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., completed_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., responses: _Optional[_Iterable[_Union[SomeServiceResponse, _Mapping]]] = ...) -> None: ...
