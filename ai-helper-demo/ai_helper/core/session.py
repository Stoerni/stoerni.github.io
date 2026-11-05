# erzeugt von scripts/build_demo.py — nicht von Hand ändern
"""Sitzung: der Gesprächsverlauf eines Gesprächs.

Der Verlauf wächst in der Reihenfolge, in der gefragt und geantwortet wird.
Der aktuelle Inhalt wird erst am Ende einer Antwort angehängt, nicht schon
beim Absenden: sonst stünde eine Frage zweimal im Verlauf.
"""

from __future__ import annotations

from collections.abc import Iterator

from ai_helper.core.message import Message, Role

__all__ = ["Session"]


class Session:
    """Hält die Nachrichten eines Gesprächs (noch ohne Speicherung auf Platte)."""

    def __init__(self, system_prompt: str | None = None) -> None:
        self._messages: list[Message] = []
        if system_prompt:
            self._messages.append(Message.system(system_prompt))

    @property
    def messages(self) -> tuple[Message, ...]:
        """Der Verlauf als unveränderliche Sicht."""
        return tuple(self._messages)

    @property
    def system_prompt(self) -> str | None:
        if self._messages and self._messages[0].role is Role.SYSTEM:
            return self._messages[0].content
        return None

    def set_system_prompt(self, content: str) -> None:
        """Setzt den Systemtext neu oder legt ihn an.

        Der Gesprächsverlauf bleibt sonst unangetastet: Persona und Gedächtnis
        ändern sich, die bisherigen Fragen und Antworten nicht.
        """
        if self._messages and self._messages[0].role is Role.SYSTEM:
            self._messages[0] = Message.system(content)
        else:
            self._messages.insert(0, Message.system(content))

    def add(self, role: Role, content: str) -> Message:
        message = Message(role, content)
        self._messages.append(message)
        return message

    def add_user(self, content: str) -> Message:
        return self.add(Role.USER, content)

    def add_assistant(self, content: str) -> Message:
        return self.add(Role.ASSISTANT, content)

    def __len__(self) -> int:
        return len(self._messages)

    def __iter__(self) -> Iterator[Message]:
        return iter(self._messages)
