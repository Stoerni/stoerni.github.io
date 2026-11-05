# erzeugt von scripts/build_demo.py — nicht von Hand ändern
"""Nachricht und Rolle.

Absichtlich der kleinstmögliche Datentyp. Der Kern tauscht nur solche
Nachrichten aus, damit später jeder Anbieter (HTTP, Ollama, llama.cpp)
und jede Hülle (Terminal, Desktop) damit arbeiten kann.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Role(str, Enum):
    """Wer eine Nachricht geschrieben hat."""

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


@dataclass(frozen=True, slots=True)
class Message:
    """Eine einzelne Nachricht im Gesprächsverlauf."""

    role: Role
    content: str

    def to_dict(self) -> dict[str, str]:
        """Darstellung für Anbieter mit OpenAI-kompatibler Schnittstelle.

        Die Rolle geht als reiner Text raus (``"user"``), nicht als Enum.
        """
        return {"role": self.role.value, "content": self.content}

    @classmethod
    def system(cls, content: str) -> "Message":
        return cls(Role.SYSTEM, content)

    @classmethod
    def user(cls, content: str) -> "Message":
        return cls(Role.USER, content)

    @classmethod
    def assistant(cls, content: str) -> "Message":
        return cls(Role.ASSISTANT, content)
