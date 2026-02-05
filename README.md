# NetOps Agent (Local, Open-Source, Synthetic)

This project is a **fully local** learning lab for agentic AI applied to NetOps. It uses **synthetic data**, **DuckDB**, and lightweight open-source Python libraries to simulate an end-to-end autonomous workflow (from incident intake to validation and ticket updates) without any external SaaS dependencies.

## What you get
- **Synthetic NetOps environment** (devices, interfaces, telemetry, incidents).
- **Agentic workflow** (plan → act → validate → update ticket).
- **RAG-style runbook retrieval** using TF‑IDF + cosine similarity stored in DuckDB.
- **No cloud dependencies**; runs on a laptop.

## Architecture (high-level)
1. **Synthetic data generator** creates devices, interfaces, metrics, and incidents.
2. **Knowledge base** loads runbooks/SOPs from `data/runbooks.yaml`.
3. **Vector index** builds TF‑IDF embeddings and persists them in DuckDB.
4. **Agent planner** matches incidents to runbooks and produces an action plan.
5. **Tool executor** simulates network commands (show interface, ping, config changes).
6. **Validator** checks the synthetic telemetry after action.
7. **Ticket updater** writes results back to DuckDB (acts as ITSM).

```
+-------------------+       +------------------+
| Synthetic Data    |       | Runbooks/SOPs    |
| (devices, logs)   |       | (YAML)           |
+---------+---------+       +---------+--------+
          |                           |
          |                           v
          |                  +--------+--------+
          |                  | Vector Index    |
          |                  | (TF-IDF + DB)   |
          v                  +--------+--------+
+---------+---------+                 |
| Incident Intake   |                 |
+---------+---------+                 v
          |                   +-------+--------+
          v                   | Agent Planner  |
+---------+---------+          +------+--------+
| Tool Executor     |                 |
+---------+---------+                 v
          |                   +-------+--------+
          v                   | Validator      |
+---------+---------+          +------+--------+
| Ticket Updater    |-----------------+
+-------------------+
```

## Tech stack (all open source)
- **Python 3.10+**
- **DuckDB** for local storage of telemetry and tickets
- **scikit‑learn** for TF‑IDF embeddings
- **Pydantic** for data models
- **Rich** for readable CLI output

## Quickstart
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .

# Run the end-to-end demo
netops-agent run
```

## Local CLI commands
- `netops-agent run` – generate synthetic data, build index, solve incidents
- `netops-agent show-db` – inspect DuckDB tables

### Viewing execution logs
The workflow writes detailed logs to `outputs/netops.log` by default. For real-time logs on the console, add `--verbose`.

```bash
netops-agent run --verbose
```

<<<<<<< codex/design-end-to-end-agentic-solution-architecture-ejerf8
### Failure scenarios and escalation
The synthetic generator marks at least one incident as a **forced failure** to demonstrate escalation. When validation fails or severity is `high`, the workflow logs an escalation event and records it in the tickets table.

=======
>>>>>>> main
## Where to start
- **Architecture**: `docs/architecture.md`
- **Runbooks**: `data/runbooks.yaml`
- **Agent flow**: `netops_agent/agent.py`
