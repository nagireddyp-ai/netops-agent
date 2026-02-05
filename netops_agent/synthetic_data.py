from __future__ import annotations

import random
from typing import List

from .models import Device, Incident, Interface

SITES = ["blr", "lhr", "iad", "sin"]
OS_VERSIONS = ["ios-xe 17.9", "ios-xe 17.6", "nx-os 10.2"]
SEVERITIES = ["low", "medium", "high"]


def make_devices(seed: int, count: int = 6) -> List[Device]:
    rng = random.Random(seed)
    devices = []
    for idx in range(count):
        devices.append(
            Device(
                device_id=f"dev-{idx+1:03d}",
                hostname=f"core-{rng.choice(SITES)}-{idx+1:02d}",
                site=rng.choice(SITES),
                os_version=rng.choice(OS_VERSIONS),
            )
        )
    return devices


def make_interfaces(seed: int, devices: List[Device]) -> List[Interface]:
    rng = random.Random(seed)
    interfaces: List[Interface] = []
    for device in devices:
        for index in range(1, 4):
            status = rng.choice(["up", "up", "down"])
            interfaces.append(
                Interface(
                    device_id=device.device_id,
                    name=f"GigabitEthernet0/{index}",
                    status=status,
                    packet_loss=round(rng.uniform(0, 15), 2),
                    error_rate=round(rng.uniform(0, 2), 2),
                )
            )
    return interfaces


def make_incidents(seed: int, interfaces: List[Interface]) -> List[Incident]:
    rng = random.Random(seed)
    incidents: List[Incident] = []
    for idx, interface in enumerate(rng.sample(interfaces, k=3)):
        if interface.status == "down":
            summary = "Interface down detected"
            category = "interfaces"
        elif interface.packet_loss > 8:
            summary = "High packet loss observed"
            category = "connectivity"
        else:
            summary = "CPU utilization high"
            category = "system"
        incidents.append(
            Incident(
                incident_id=f"inc-{idx+1:04d}",
                device_id=interface.device_id,
                interface=interface.name,
                summary=summary,
                category=category,
                severity=rng.choice(SEVERITIES),
                gateway="10.0.0.1",
            )
        )
    return incidents
