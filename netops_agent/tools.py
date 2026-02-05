from __future__ import annotations

from dataclasses import dataclass

from .models import Incident


@dataclass
class ToolResult:
    command: str
    output: str


def show_interface(incident: Incident) -> ToolResult:
    command = f"show interface {incident.interface}"
    output = f"{incident.interface} is up with healthy counters"
    return ToolResult(command=command, output=output)


def show_interface_counters(incident: Incident) -> ToolResult:
    command = f"show interface {incident.interface} counters"
    output = "Errors: 0, Drops: 1"
    return ToolResult(command=command, output=output)


def ping_gateway(incident: Incident) -> ToolResult:
    command = f"ping {incident.gateway} count 5"
    output = "Success rate 100 percent"
    return ToolResult(command=command, output=output)


def reset_interface(incident: Incident) -> ToolResult:
    command = f"interface {incident.interface} ; shutdown ; no shutdown"
    output = "Interface reset completed"
    return ToolResult(command=command, output=output)


def show_process_cpu() -> ToolResult:
    command = "show process cpu"
    output = "CPU utilization 45%"
    return ToolResult(command=command, output=output)
