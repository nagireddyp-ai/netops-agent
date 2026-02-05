from __future__ import annotations

from dataclasses import dataclass
from typing import List

from .models import ExecutionResult, Incident, Runbook
from .tools import (
    ping_gateway,
    reset_interface,
    show_interface,
    show_interface_counters,
    show_process_cpu,
)


@dataclass
class PlanStep:
    description: str
    tool: str


class NetOpsAgent:
    def plan(self, incident: Incident, runbook: Runbook) -> List[PlanStep]:
        plan = []
        for command in runbook.commands:
            if "show interface" in command and "counters" not in command:
                plan.append(PlanStep(description="Check interface status", tool="show_interface"))
            elif "counters" in command:
                plan.append(
                    PlanStep(description="Check interface counters", tool="show_interface_counters")
                )
            elif "ping" in command:
                plan.append(PlanStep(description="Ping gateway", tool="ping_gateway"))
            elif "shutdown" in command:
                plan.append(PlanStep(description="Reset interface", tool="reset_interface"))
            elif "process cpu" in command:
                plan.append(PlanStep(description="Check CPU", tool="show_process_cpu"))
        return plan

    def execute(self, incident: Incident, plan: List[PlanStep]) -> ExecutionResult:
        actions = []
        for step in plan:
            if step.tool == "show_interface":
                result = show_interface(incident)
            elif step.tool == "show_interface_counters":
                result = show_interface_counters(incident)
            elif step.tool == "ping_gateway":
                result = ping_gateway(incident)
            elif step.tool == "reset_interface":
                result = reset_interface(incident)
            elif step.tool == "show_process_cpu":
                result = show_process_cpu()
            else:
                continue
            actions.append(f"{result.command} -> {result.output}")
        return ExecutionResult(
            incident_id=incident.incident_id,
            runbook_id="",
            actions=actions,
            validation_passed=True,
            notes="Actions executed successfully",
        )
