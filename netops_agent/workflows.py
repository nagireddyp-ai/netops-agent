from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List

from rich.console import Console
from rich.table import Table

from .agent import NetOpsAgent
from .db import NetOpsDatabase
from .models import ExecutionResult, Incident
from .rag import RunbookIndex
from .synthetic_data import make_devices, make_incidents, make_interfaces


@dataclass
class RunContext:
    seed: int
    db_path: str = "outputs/netops.duckdb"


class NetOpsWorkflow:
    def __init__(self, context: RunContext) -> None:
        self.context = context
        self.console = Console()
        self.db = NetOpsDatabase(context.db_path)
        self.index = RunbookIndex(context.db_path)
        self.agent = NetOpsAgent()

    def prepare_data(self) -> List[Incident]:
        devices = make_devices(self.context.seed)
        interfaces = make_interfaces(self.context.seed, devices)
        incidents = make_incidents(self.context.seed, interfaces)
        self.db.init_schema()
        self.db.load_devices(devices)
        self.db.load_interfaces(interfaces)
        self.db.load_incidents(incidents)
        return incidents

    def build_index(self) -> None:
        self.index.load_runbooks(Path("data/runbooks.yaml"))
        self.index.build()
        self.index.persist()

    def run_incident(self, incident: Incident) -> ExecutionResult:
        runbook, score = self.index.query(incident.summary, top_k=1)[0]
        plan = self.agent.plan(incident, runbook)
        result = self.agent.execute(incident, plan)
        result.runbook_id = runbook.runbook_id
        result.notes = f"Matched runbook {runbook.title} (score {score:.2f})."
        self.db.write_ticket(result.incident_id, result.runbook_id, result.notes, result.validation_passed)
        return result

    def run(self) -> None:
        incidents = self.prepare_data()
        self.build_index()
        results = [self.run_incident(incident) for incident in incidents]
        self._render_results(results)

    def _render_results(self, results: List[ExecutionResult]) -> None:
        table = Table(title="NetOps Agent Results")
        table.add_column("Incident")
        table.add_column("Runbook")
        table.add_column("Validation")
        table.add_column("Notes")
        for result in results:
            table.add_row(
                result.incident_id,
                result.runbook_id,
                "PASS" if result.validation_passed else "FAIL",
                result.notes,
            )
        self.console.print(table)
