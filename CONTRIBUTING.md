# Contributing to NEXUS

Thank you for contributing to NEXUS.

NEXUS is a local-first developer intelligence platform built around modular MCP providers, contextual AI summaries, and low-cognitive-overhead operational design.

The architecture is intentionally designed so new data sources can be added independently without rewriting the core system.

---

# Project Philosophy

Before contributing, understand the core design principles behind NEXUS.

NEXUS prioritizes:

- Local-first execution
- Modular provider boundaries
- Graceful degradation
- Low cognitive overhead
- Focused operational UX
- Optional AI augmentation
- Reliability over feature count


The default implementation prioritizes:

- focused
- clear
- modular
- operational
- low-noise

Every contribution should improve contextual awareness without increasing unnecessary complexity.

---

# Architecture Overview

```text
MCP Providers
├── GitHub
├── LeetCode
└── Fitness
        ↓

FastAPI Aggregation Layer
├── async orchestration
├── provider isolation
├── SQLite persistence
└── optional Ollama summaries
        ↓

React Frontend
├── operational dashboard
├── provider sections
└── adaptive metric rendering
```

---

# Repo Structure

```text
nexus/
├── backend/
│   └── app/
│       ├── routers/
│       │   └── dashboard.py
│       ├── config.py
│       ├── db.py
│       ├── mcp_client.py
│       └── ollama_client.py
│
├── frontend/
│   └── src/
│       ├── components/
│       ├── hooks/
│       ├── App.tsx
│       └── types.ts
│
├── mcp-servers/
│   ├── github/
│   ├── leetcode/
│   └── fitness/
│
├── docs/
├── CONTRIBUTING.md
├── README.md
└── Makefile
```

---

# Development Setup

## 1. Clone Repository

```bash
git clone https://github.com/Acestar21/nexus.git
cd nexus
```

---

## 2. Configure Environment

```bash
cp .env.example .env
```

Fill in required environment variables.

---

## 3. Install Dependencies

```bash
make install
```

---

## 4. Start Development Environment

```bash
make dev
```

Frontend:

```text
http://localhost:5173
```

Backend:

```text
http://localhost:8000
```

---

# Adding a New MCP Provider

NEXUS is intentionally provider-driven.

A new data source should generally mean:

```text
one new provider folder
```

NOT:

```text
rewriting backend infrastructure
```

Follow the existing patterns in:

* `mcp-servers/github/`
* `mcp-servers/leetcode/`
* `mcp-servers/fitness/`

---

# Step 1 — Create Provider Folder

```text
mcp-servers/your-provider/
├── server.py
├── models.py
└── requirements.txt
```

---

# Step 2 — Define Provider Models

Example:

```python
from datetime import datetime
from pydantic import BaseModel

class YourActivity(BaseModel):
    metric_one: int
    metric_two: int

class YourSnapshot(BaseModel):
    captured_at: datetime
    activity: YourActivity
```

---

# Step 3 — Implement MCP Server

Example:

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("your-provider")

@mcp.tool()
async def get_activity() -> str:
    ...
    return snapshot.model_dump_json()

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

---

# Step 4 — Test Provider Standalone

```bash
mcp dev mcp-servers/your-provider/server.py
```

Providers should always be independently runnable and testable.

---

# Step 5 — Register Provider in Backend

In:

```text
backend/app/routers/dashboard.py
```

Add:

```python
provider_data, provider_err = await safe_call_tool(
    "your-provider",
    "get_activity"
)
```

Then:

* add provider data to response payload
* handle degraded state in frontend
* ensure partial rendering still works

---

# Provider Contract Expectations

Providers should:

* expose narrowly scoped tools
* return serialized Pydantic models
* include timestamps where relevant
* avoid frontend-specific formatting
* keep business logic inside provider layer
* fail gracefully with meaningful error context

---

# Example Provider Output

Example serialized snapshot:

```json
{
  "captured_at": "2026-05-18T10:15:00",
  "activity": {
    "current_streak": 12,
    "problems_today": 2
  }
}
```

---

## Provider Flexibility

Providers can be implemented in any language with MCP SDK support as long as they expose compatible MCP tools and can be orchestrated by the backend.

The provider contract described above reflects the default implementation pattern used throughout NEXUS for consistency and maintainability.

Alternative provider implementations and architectures are completely acceptable for personal forks and standalone integrations.

However, contributions intended for the main NEXUS repository should follow the established provider contract and project structure to preserve consistency across the ecosystem.
---

# Reliability Expectations

NEXUS is designed around graceful degradation.

This means:

* one failing provider should never crash the dashboard
* provider failures should remain isolated
* stale snapshots are preferred over blank states where possible
* operational state should remain visible to the user

Avoid:

* global failures
* hidden exceptions
* silent data corruption

---

# Frontend Guidelines

## Dashboard Philosophy

The UI should remain:

* focused
* operational
* low-noise
* fast to scan

The reference implementation prioritizes:
- fast scanability
- operational clarity
- focused telemetry presentation

Contributors are encouraged to experiment with alternative visual approaches where appropriate.

---

# Important Frontend Files

## Layout & Styling

```text
frontend/src/index.css
```

---

## Main Dashboard

```text
frontend/src/App.tsx
```

---

## Metric Cards

```text
frontend/src/components/MetricCard.tsx
```

---

# Grid System

The metrics grid uses:

```css
repeat(auto-fit, minmax(200px, 1fr))
```

New metric cards automatically adapt to layout width.

Do not hardcode fixed-width dashboard layouts.

---

# AI Layer Guidelines

The AI layer should:

* contextualize
* prioritize
* summarize patterns

It should NOT:

* generate generic motivation
* behave like a chatbot
* dominate the product experience

Good:

```text
GitHub activity declined relative to weekly average while workout consistency remained stable.
```

Bad:

```text
Keep going! You’re doing great!
```

NEXUS should feel:

```text
analytical
```

NOT:

```text
motivational
```

---

# Coding Standards

## Backend

* Type hints everywhere
* Async throughout backend
* Pydantic models for contracts
* Explicit error handling
* Logging via `logging`
* No silent failures
* No blocking I/O inside async routes

---

## Frontend

* Keep components small
* Avoid unnecessary state complexity
* Preserve low-cognitive-overhead UX
* Prefer clarity over visual density

---

# Dependency Philosophy

NEXUS intentionally minimizes dependencies.

Before adding a dependency:

* ask whether native platform APIs already solve the problem
* consider maintenance overhead
* consider security implications
* avoid dependency bloat

---

# Security Practices

Do NOT:

* commit credentials
* expose filesystem paths in UI
* log secrets
* hardcode tokens

Always:

* validate external data
* handle provider failures safely
* keep sensitive config in `.env`

---

# Pull Request Guidelines

Before opening a PR:

* ensure fresh setup works
* run formatting/linting
* test provider independently
* verify dashboard still renders under partial provider failure
* avoid unrelated architectural rewrites

---

# What Contributions Are Most Valuable

High-value contributions:

* new MCP providers
* reliability improvements
* onboarding improvements
* historical telemetry analysis
* trend analysis
* provider health systems
* documentation improvements
* accessibility improvements

Lower-value contributions:

* random widgets
* excessive animations
* social/gamification features
* generic AI chat interfaces

---

# Design Direction

The default NEXUS implementation prioritizes:

- local-first execution
- modular provider boundaries
- operational clarity
- resilient orchestration
- focused telemetry presentation

Areas of future exploration may include:

- richer historical analysis
- improved operational summarization
- provider ecosystem expansion
- stronger reliability tooling
- better operational awareness

The project intentionally avoids:
- feature-heavy productivity clutter
- generic AI chat interfaces
- unnecessary dashboard complexity
- cloud-dependent architecture


# Questions / Discussions

If you want to discuss:

* architecture
* provider ideas
* major refactors
* ecosystem direction

open a discussion or issue before implementing large changes.

---

Built and maintained by Kushal Singh Kushwaha.

