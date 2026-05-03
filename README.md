# SmartEat MAS (Multi-Agent System)

SmartEat MAS is a **locally hosted multi-agent food ordering assistant** developed for the **Current Trends in Software Engineering (CTSE) Assignment 2**.  
The system demonstrates how multiple AI agents can collaborate to process a natural language food request, search local restaurant data, create an order draft, generate a user response, and record execution traces.

---

## Project Overview

This project reuses the **SmartEat food ordering domain** from Assignment 1 and extends it into a **Multi-Agent System (MAS)** architecture.

The system is built entirely for **local execution** and uses:

- **LangGraph** for multi-agent orchestration
- **Ollama** for local Small Language Model (SLM) support
- **SQLite** for local data storage
- **FastAPI** for the local API
- **Streamlit** for the demo UI
- **Pytest** for evaluation and testing
- **JSONL logging** for observability and execution tracing

---

## Multi-Agent Architecture

SmartEat MAS contains **4 specialized agents**:

1. **User Preference Agent**
   - Loads user profile
   - Extracts request constraints
   - Merges user preferences

2. **Restaurant Discovery Agent**
   - Searches restaurants
   - Filters by cuisine, budget, location, halal, and vegetarian requirements

3. **Order Management Agent**
   - Loads menu data
   - Selects valid items
   - Creates an order draft

4. **Notification Agent**
   - Generates the final response
   - Saves notifications
   - Writes order summary files

All agents share a common global state object called **SmartEatState**, and the workflow is orchestrated using **LangGraph**.

---

## Features

- Multi-agent food ordering workflow using **4 connected agents**
- **LangGraph orchestration** with shared state passing
- **Local Ollama model integration** for grounded agent reasoning
- **Custom Python tools** for database and file interactions
- **SQLite database** for users, restaurants, menu items, orders, and notifications
- **FastAPI API** for local execution and Swagger testing
- **Streamlit UI** for demo presentation
- **JSONL trace logging** for observability
- **Pytest-based testing and evaluation**
- Local output generation for **order summaries** and **trace logs**

---

## Project Structure

```text
smarteat-mas/
│
├── app/
│   ├── agents/                  # Agent implementations and prompt helpers
│   ├── api/                     # FastAPI application
│   ├── data/                    # Sample JSON seed data
│   ├── database/                # SQLite DB helpers and initialization
│   ├── graph/                   # LangGraph state and workflow
│   ├── llm/                     # Ollama client wrapper
│   ├── logging/                 # Trace logging utilities
│   ├── output/order_summaries/  # Generated order summary files
│   ├── tools/                   # Custom Python tools used by agents
│   └── ui/                      # Streamlit demo UI
│
├── logs/                        # Generated trace.jsonl logs
├── tests/                       # Unit and workflow tests
├── requirements.txt
├── .env
└── README.md