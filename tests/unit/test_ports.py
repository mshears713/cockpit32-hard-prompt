"""Fake-first tests for port discovery."""

from cockpit32.core.ports import PortInfo, PortLister


class FakePortLister:
    def __init__(self, ports: list[PortInfo]):
        self._ports = ports

    def list_ports(self) -> list[PortInfo]:
        return self._ports


def test_fake_port_lister_satisfies_protocol():
    lister: PortLister = FakePortLister([PortInfo(device="COM3", description="USB Serial")])
    ports = lister.list_ports()
    assert ports == [PortInfo(device="COM3", description="USB Serial")]


def test_port_info_defaults_description_to_empty_string():
    assert PortInfo(device="/dev/ttyUSB0").description == ""
