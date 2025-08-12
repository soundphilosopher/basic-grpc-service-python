import re
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

@dataclass
class ReplyResult:
    text: str
    goodbye: bool

class Utils:
    class Talk:
        GOODBYE_INPUT_SET = {"bye", "exit", "goodbye", "quit"}

        GOODBYE_RESPONSES = [
            "Goodbye. It was nice talking to you.",
            "Thank you for talking with me.",
            "Thank you, that will be $150. Have a good day!",
            "Goodbye. This was really a nice talk.",
            "Goodbye. I'm looking forward to our next session.",
            "This was a good session, wasn't it – but time is over now. Goodbye.",
            "Maybe we could discuss this over more in our next session? Goodbye.",
            "Good-bye."
        ]

        REQUEST_INPUT_REGEX_TO_RESPONSE_OPTIONS: List[Tuple[Pattern, List[str]]] = [
            (re.compile(r"^i need (.*)$"), [
                "Why do you need %s?",
                "Would it really help you to get %s?",
                "Are you sure you need %s?"
            ]),
            (re.compile(r"^why don'?t you ([^?]*)\??$"), [
                "Do you really think I don't %s?",
                "Perhaps eventually I will %s.",
                "Do you really want me to %s?"
            ]),
            (re.compile(r"^why can'?t i ([^?]*)\??$"), [
                "Do you think you should be able to %s?",
                "If you could %s, what would you do?",
                "I don't know -- why can't you %s?",
                "Have you really tried?"
            ]),
            # ... translate all other regex/response pairs exactly ...
        ]

        DEFAULT_RESPONSES = [
            "Please tell me more.",
            "Let's change focus a bit...Tell me about your family.",
            "Can you elaborate on that?",
            "I see.",
            "Very interesting.",
            "I see. And what does that tell you?",
            "How does that make you feel?",
            "How do you feel when you say that?"
        ]

        REFLECTED_WORDS = {
            "am": "are",
            "was": "were",
            "i": "you",
            "i'd": "you would",
            "i've": "you have",
            "i'll": "you will",
            "my": "your",
            "are": "am",
            "you've": "I have",
            "you'll": "I will",
            "your": "my",
            "yours": "mine",
            "you": "me",
            "me": "you"
        }

        INTRO_RESPONSES = [
            "Hi %s. I'm just a greeter.",
            "Before we begin, %s, let me tell you something about myself."
        ]

        FACTS = [
            "I was created by Joseph Weizenbaum.",
            "I was created in the 1960s.",
            "I am a Rogerian psychotherapist.",
            "I am named after Eliza Doolittle from the play Pygmalion.",
            "I was originally written on an IBM 7094.",
            "I can be accessed in most Emacs implementations with the command M-x doctor.",
            "I was created at the MIT Artificial Intelligence Laboratory.",
            "I was one of the first programs capable of attempting the Turing test.",
            "I was designed as a method to show the superficiality of communication between man and machine."
        ]

        def __init__(self, rng: Optional[random.Random] = None):
            self.rng = rng or random.Random()

        def reply(self, input_str: str) -> ReplyResult:
            norm = self.preprocess(input_str)
            if norm in self.GOODBYE_INPUT_SET:
                return ReplyResult(self.sample(self.GOODBYE_RESPONSES), True)
            return ReplyResult(self.lookup_response(norm), False)

        def get_intro_responses(self, name: str) -> List[str]:
            intros = [tpl % name for tpl in self.INTRO_RESPONSES]
            intros.append(self.sample(self.FACTS))
            intros.append("How are you feeling today?")
            return intros

        def preprocess(self, input_str: str) -> str:
            s = str(input_str).strip().lower()
            # strip leading/trailing punctuation .,!?'"
            return re.sub(r'^[\.!?\"]+|[\.!?\"]+$', '', s)

        def sample(self, items: List[str]) -> str:
            return self.rng.choice(items)

        def reflect(self, fragment: str) -> str:
            return " ".join(self.REFLECTED_WORDS.get(w, w) for w in fragment.split())

        def lookup_response(self, input_str: str) -> str:
            for pattern, responses in self.REQUEST_INPUT_REGEX_TO_RESPONSE_OPTIONS:
                match = pattern.match(input_str)
                if match:
                    response = self.sample(responses)
                    if "%s" not in response:
                        return response
                    if match.group(1):
                        frag = self.reflect(match.group(1))
                        return response.replace("%s", frag)
            return self.sample(self.DEFAULT_RESPONSES)

    class Some:
        def build_background_response(self, *, state, started_at, completed_at, responses):
            """
            Build a Basic::Service::V1::BackgroundResponse populated with a CloudEvent
            that wraps a BackgroundResponseEvent payload.
            """
            payload = service_pb2.BackgroundResponseEvent(
                state=state,
                started_at=self._to_ts(started_at),
                completed_at=self._to_ts(completed_at) if completed_at else None,
                responses=responses,  # pass through a list of Response messages
            )

            any_msg = Any()
            # Packs payload and sets type_url to "type.googleapis.com/<full.name>"
            any_msg.Pack(payload)

            now_ts = self._to_ts(dt.datetime.now(dt.timezone.utc))

            ce = CloudEvent(
                id=str(uuid.uuid4()),
                source="urn:service:basic",
                spec_version="1.0",  # matches your Ruby
                type=payload.DESCRIPTOR.full_name,  # fully-qualified message name
                attributes={
                    "time": CloudEvent.CloudEventAttributeValue(ce_timestamp=now_ts),
                },
                proto_data=any_msg,
            )

            return service_pb2.BackgroundResponse(cloud_event=ce)

        def fake_service_response(self, name, protocol):
            """
            Simulate work and return a SomeServiceResponse populated with SomeServiceData.
            """
            _time.sleep(random.uniform(1.0, 3.0))

            return service_pb2.SomeServiceResponse(
                id=str(uuid.uuid4()),
                name=name,
                version="v1",
                data=service_pb2.SomeServiceData(
                    value=str(protocol),
                    type="protocol",
                ),
            )

        def _to_ts(self, when):
            """
            Convert a datetime or epoch seconds (float/int) to google.protobuf.Timestamp.
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
