from __future__ import annotations

from pathlib import Path
from typing import Iterable

import duckdb
import pandas as pd

from .models import Device, Incident, Interface


class NetOpsDatabase:
    def __init__(self, path: str = "outputs/netops.duckdb") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = duckdb.connect(str(self.path))

    def init_schema(self) -> None:
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS devices (
                device_id VARCHAR PRIMARY KEY,
                hostname VARCHAR,
                site VARCHAR,
                os_version VARCHAR
            );
            """
        )
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS interfaces (
                device_id VARCHAR,
                name VARCHAR,
                status VARCHAR,
                packet_loss DOUBLE,
                error_rate DOUBLE
            );
            """
        )
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS incidents (
                incident_id VARCHAR PRIMARY KEY,
                device_id VARCHAR,
                interface VARCHAR,
                summary VARCHAR,
                category VARCHAR,
                severity VARCHAR,
<<<<<<< codex/design-end-to-end-agentic-solution-architecture-ejerf8
                gateway VARCHAR,
                should_fail BOOLEAN,
                failure_reason VARCHAR
=======
                gateway VARCHAR
>>>>>>> main
            );
            """
        )
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tickets (
                incident_id VARCHAR,
                runbook_id VARCHAR,
                notes VARCHAR,
<<<<<<< codex/design-end-to-end-agentic-solution-architecture-ejerf8
                validation_passed BOOLEAN,
                validation_reason VARCHAR,
                escalated BOOLEAN
=======
                validation_passed BOOLEAN
>>>>>>> main
            );
            """
        )

    def load_devices(self, devices: Iterable[Device]) -> None:
        df = pd.DataFrame([d.model_dump() for d in devices])
        self.conn.execute("DELETE FROM devices")
        self.conn.register("devices_df", df)
        self.conn.execute("INSERT INTO devices SELECT * FROM devices_df")

    def load_interfaces(self, interfaces: Iterable[Interface]) -> None:
        df = pd.DataFrame([i.model_dump() for i in interfaces])
        self.conn.execute("DELETE FROM interfaces")
        self.conn.register("interfaces_df", df)
        self.conn.execute("INSERT INTO interfaces SELECT * FROM interfaces_df")

    def load_incidents(self, incidents: Iterable[Incident]) -> None:
        df = pd.DataFrame([i.model_dump() for i in incidents])
        self.conn.execute("DELETE FROM incidents")
        self.conn.register("incidents_df", df)
        self.conn.execute("INSERT INTO incidents SELECT * FROM incidents_df")

<<<<<<< codex/design-end-to-end-agentic-solution-architecture-ejerf8
    def write_ticket(
        self,
        incident_id: str,
        runbook_id: str,
        notes: str,
        passed: bool,
        reason: str,
        escalated: bool,
    ) -> None:
        self.conn.execute(
            "INSERT INTO tickets VALUES (?, ?, ?, ?, ?, ?)",
            [incident_id, runbook_id, notes, passed, reason, escalated],
=======
    def write_ticket(self, incident_id: str, runbook_id: str, notes: str, passed: bool) -> None:
        self.conn.execute(
            "INSERT INTO tickets VALUES (?, ?, ?, ?)",
            [incident_id, runbook_id, notes, passed],
>>>>>>> main
        )

    def show_tables(self) -> dict[str, pd.DataFrame]:
        tables = {}
        for table in ["devices", "interfaces", "incidents", "tickets"]:
            tables[table] = self.conn.execute(f"SELECT * FROM {table}").df()
        return tables
