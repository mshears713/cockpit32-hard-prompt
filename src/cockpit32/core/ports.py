"""Serial port discovery.

Engineering Method Selection: fake-first. Real COM-port enumeration
depends on pyserial and physical hardware, both outside the agent's
environment in Stage 3 — see docs/validation for the Deferred entry.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass
class PortInfo:
    device: str
    description: str = ""


class PortLister(Protocol):
    def list_ports(self) -> list[PortInfo]: ...


class PyserialPortLister:
    """Real lister. Requires pyserial (the `serial` extra); falls back to
    an empty list with a clear reason if pyserial isn't installed.
    """

    def list_ports(self) -> list[PortInfo]:
        try:
            from serial.tools import list_ports as _list_ports
        except ImportError:
            return []
        return [
            PortInfo(device=p.device, description=p.description or "")
            for p in _list_ports.comports()
        ]


def pyserial_available() -> bool:
    try:
        import serial  # noqa: F401
    except ImportError:
        return False
    return True
