from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field


class Device(BaseModel):
    device_id: str
    hostname: str
    site: str
    os_version: str


class Interface(BaseModel):
    device_id: str
    name: str
    status: str
    packet_loss: float = 0.0
    error_rate: float = 0.0


class Incident(BaseModel):
    incident_id: str
    device_id: str
    interface: str
    summary: str
    category: str
    severity: str
    gateway: str


class Runbook(BaseModel):
    runbook_id: str = Field(alias="id")
    title: str
    category: str
    steps: List[str]
    commands: List[str]
    validation: List[str]


class ExecutionResult(BaseModel):
    incident_id: str
    runbook_id: str
    actions: List[str]
    validation_passed: bool
    notes: str
