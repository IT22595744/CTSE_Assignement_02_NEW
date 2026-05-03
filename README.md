
# SmartEat MAS (Multi-Agent System)

Lightweight multi-agent restaurant ordering demo used for CTSE assignments.

## Summary

This repository contains a small multi-agent system that simulates restaurant ordering, notifications, and simple workflows. It is implemented in Python and includes tests and a minimal Streamlit UI.

## Contents

- `app/` - main application code, agents, API, tools, and UI.
- `app/data/` - sample `menus.json`, `restaurants.json`, and `users.json`.
- `app/database/` - database helpers and initialization scripts.
- `app/graph/` - state and workflow logic for the agent graph.
- `app/llm/` - small client wrappers for local LLM usage.
- `app/logging/` - tracing and logging utilities.
- `app/output/order_summaries/` - generated order summary outputs.
- `tests/` - unit and integration tests.


## Features

- Multi-agent restaurant ordering workflow with user, restaurant, order, and notification agents
- Local LLM integration for prompt-based behavior
- Simple Streamlit UI for demo interactions
- Built-in tests covering agent behavior, notifications, and workflow logic
- Output generation for order summaries in `app/output/order_summaries/`

## Requirements

- Python 3.10 or newer
- See `requirements.txt` for Python dependencies.

## Quick setup

1. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

3. (Optional) Create a `.env` file to add environment variables used by the app.

## Running

- Run the API (if available):

```powershell
python -m app.api.main
```

- Run the Streamlit UI (simple demo):

```powershell
streamlit run app/ui/streamlit_app.py
```

## Tests

Run the test suite with `pytest` from the repository root:

```powershell
pytest -q
```

## Project notes

- The agent implementations live under `app/agents/`.
- Order output files are written to `app/output/order_summaries/`.
- If you want me to explain a specific file, run tests, or fix failing tests, tell me which file or say "run tests".

---

Updated README to include setup and run instructions.
