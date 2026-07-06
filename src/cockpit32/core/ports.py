from __future__ import annotations

from dataclasses import dataclass

try:
    from serial.tools import list_ports
except ImportError:  # pyserial is a runtime dependency; doctor reports if unavailable.
    list_ports = None


@dataclass(frozen=True)
class PortInfo:
    device: str
    description: str


def discover_ports() -> list[PortInfo]:
    if list_ports is None:
        return []
    return [PortInfo(port.device, port.description) for port in list_ports.comports()]
