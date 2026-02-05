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
    log_path: str = "outputs/netops.log"
    verbose: bool = False


class NetOpsWorkflow:
    def __init__(self, context: RunContext) -> None:
        self.context = context
        self.console = Console()
        self.db = NetOpsDatabase(context.db_path)
        self.index = RunbookIndex(context.db_path)
        self.agent = NetOpsAgent()
        self.logger = self._setup_logger()

    def _setup_logger(self) -> "logging.Logger":
        import logging

        logger = logging.getLogger("netops-agent")
        logger.setLevel(logging.INFO)
        logger.handlers.clear()
        formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

        log_path = Path(self.context.log_path)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_path)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        if self.context.verbose:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

        return logger

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
        self.logger.info(
            "[PLAN] %s matched runbook %s (score %.2f)",
            incident.incident_id,
            runbook.runbook_id,
            score,
        )
        for step in runbook.steps:
            self.logger.info("[STEP] %s %s", incident.incident_id, step)
        plan = self.agent.plan(incident, runbook)
        result = self.agent.execute(incident, plan, logger=self.logger.info)
        result.runbook_id = runbook.runbook_id
<<<<<<< codex/design-end-to-end-agentic-solution-architecture-ejerf8
        result.validation_passed = not incident.should_fail
        result.validation_reason = (
            "Synthetic validation failed"
            if incident.should_fail
            else "Synthetic validation passed"
        )
        result.escalated = (not result.validation_passed) or incident.severity == "high"
        result.notes = f"Matched runbook {runbook.title} (score {score:.2f})."
        self.logger.info(
            "[VALIDATION] %s %s (%s)",
            result.incident_id,
            "PASS" if result.validation_passed else "FAIL",
            result.validation_reason,
        )
        if result.escalated:
            self.logger.info(
                "[ESCALATION] %s escalated to human. reason=%s severity=%s",
                result.incident_id,
                incident.failure_reason or "Policy escalation",
                incident.severity,
            )
        self.db.write_ticket(
            result.incident_id,
            result.runbook_id,
            result.notes,
            result.validation_passed,
            result.validation_reason,
            result.escalated,
        )
=======
        result.notes = f"Matched runbook {runbook.title} (score {score:.2f})."
        self.db.write_ticket(result.incident_id, result.runbook_id, result.notes, result.validation_passed)
>>>>>>> main
        self.logger.info(
            "[RESULT] %s validation=%s runbook=%s",
            result.incident_id,
            "PASS" if result.validation_passed else "FAIL",
            result.runbook_id,
        )
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
<<<<<<< codex/design-end-to-end-agentic-solution-architecture-ejerf8
        table.add_column("Escalation")
=======
>>>>>>> main
        table.add_column("Notes")
        for result in results:
            table.add_row(
                result.incident_id,
                result.runbook_id,
                "PASS" if result.validation_passed else "FAIL",
<<<<<<< codex/design-end-to-end-agentic-solution-architecture-ejerf8
                "YES" if result.escalated else "NO",
=======
>>>>>>> main
                result.notes,
            )
        self.console.print(table)
