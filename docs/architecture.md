# Solution Architecture (Local Agentic NetOps)

## Overview
This solution is a **local-only, open-source** agentic NetOps lab. It simulates the end-to-end flow using synthetic data, then executes an automated remediation workflow that mirrors a real NOC process. There are no external APIs or closed-source tools.

## Key components
1. **Synthetic Data Factory**
   - Generates devices, interfaces, telemetry, and incidents.
   - Ensures deterministic replay via a random seed.

2. **Knowledge Base (Runbooks)**
   - YAML documents containing SOPs and remediation steps.
   - Indexed via TF‑IDF embeddings and stored in DuckDB.

3. **Agent Orchestrator**
   - **Planner**: maps incidents to runbooks using vector similarity.
   - **Executor**: runs simulated network commands (show interface, ping, config).
   - **Validator**: checks post-action synthetic metrics.
   - **Reporter**: writes remediation notes and results to tickets.

4. **Storage**
   - **DuckDB** for telemetry, tickets, and runbooks.
   - No external databases required.

## End-to-end flow
1. Generate synthetic devices and telemetry.
2. Inject incidents (e.g., interface flaps, packet loss, CPU spikes).
3. Agent retrieves best matching runbook from the knowledge base.
4. Agent executes the simulated commands.
5. Validator confirms the state is improved.
6. Ticket is updated with actions and results.

## Tech decisions
- **DuckDB** keeps everything local and fast.
- **TF‑IDF** keeps the vector search lightweight and offline.
- **Pydantic** enforces strong data validation.
- **Rich CLI** provides readable outputs for learning.

## Extension ideas
- Swap TF‑IDF with **ChromaDB** + sentence-transformers for stronger retrieval.
- Plug in **llama-cpp** or **Ollama** for local LLM reasoning.
- Add realistic network device emulation using **Containerlab**.
