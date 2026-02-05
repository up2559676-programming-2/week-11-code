from dataclasses import dataclass, field
from typing import ClassVar, Protocol


@dataclass
class Message:
    _last_id: ClassVar[int] = 0

    id: int = field(init=False, default=-1)
    author: "User"
    content: str

    def __post_init__(self):
        self.__class__._last_id += 1
        self.id = self._last_id


class User(Protocol):
    messages: list[Message]
    pins_ref: list[Message]

    def _find_msg_by_id(self, id: int) -> Message | None:
        for msg in self.messages:
            if msg.id == id:
                return msg
        return None

    def send_message(self, content: str) -> Message: ...

    def pin_message(self, id: int) -> None: ...


class Unverified(User):
    def __init__(self) -> None:
        self.messages: list[Message] = []
        self.pins_ref: list[Message] = []

    def send_message(self, content: str) -> Message:
        raise PermissionError("401: Unauthorized")

    def pin_message(self, id: int) -> None:
        raise PermissionError("401: Unauthorized")


class Verified(User):
    def __init__(self) -> None:
        self.messages: list[Message] = []
        self.pins_ref: list[Message] = []

    def send_message(self, content: str) -> Message:
        if len(content) > 100:
            raise ValueError(
                "Maximum message length exceeded. Upgrade to Nitro for unlimited message length."
            )

        msg = Message(self, content)
        self.messages.append(msg)
        return msg

    def pin_message(self, id: int) -> None:
        raise PermissionError("401: Unauthorized")


class Nitro(User):
    def __init__(self) -> None:
        self.messages: list[Message] = []
        self.pins_ref: list[Message] = []

    def send_message(self, content: str) -> Message:
        msg = Message(self, content)
        self.messages.append(msg)
        return msg

    def pin_message(self, id: int) -> None:
        message = self._find_msg_by_id(id)
        if message is None:
            raise ValueError(f"Message {id} does not exist in this channel")

        self.messages.insert(0, message)
        self.pins_ref.append(message)


def test():
    # --- setup users ---
    unverified = Unverified()
    verified = Verified()
    nitro = Nitro()

    # required attributes
    for u in (unverified, verified, nitro):
        u.messages = []
        u.pins_ref = []

    # --- Unverified user ---
    try:
        unverified.send_message("hello")
        assert False
    except PermissionError:
        pass

    try:
        unverified.pin_message(1)
        assert False
    except PermissionError:
        pass

    assert unverified.messages == []
    assert unverified.pins_ref == []

    # --- Verified user ---
    msg_ok = verified.send_message("a" * 100)
    assert msg_ok.content == "a" * 100
    assert msg_ok.author is verified
    assert msg_ok in verified.messages

    try:
        verified.send_message("a" * 101)
        assert False
    except ValueError:
        pass

    try:
        verified.pin_message(msg_ok.id)
        assert False
    except PermissionError:
        pass

    assert verified.pins_ref == []

    # --- Nitro user ---
    long_msg = nitro.send_message("x" * 10_000)
    assert long_msg.content == "x" * 10_000
    assert long_msg.author is nitro
    assert long_msg in nitro.messages

    # pinning works
    nitro.pin_message(long_msg.id)
    assert long_msg in nitro.pins_ref

    # pinned messages must appear first
    second_msg = nitro.send_message("normal message")
    ordered = nitro.pins_ref + [m for m in nitro.messages if m not in nitro.pins_ref]

    assert ordered[0] is long_msg
    assert ordered[1] is second_msg

    # --- Message IDs must be unique globally ---
    ids = {
        msg_ok.id,
        long_msg.id,
        second_msg.id,
    }
    assert len(ids) == 3


test()
