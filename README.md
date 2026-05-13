# Nexus — Personal Life Dashboard

A self-hosted, open source personal command center powered by MCP servers and a local AI. Aggregates your GitHub activity, fitness logs, and daily goals into a single minimal dashboard with an AI-generated morning brief.

No cloud. No tracking. Runs entirely on your machine.

![Dashboard Preview](docs/preview.png)

---

## How It Works
```
MCP Servers (Python, stdio transport)
├── github/     → GraphQL contributions API
├── fitness/    → local workout log
└── leetcode/   → (coming soon)
↓
FastAPI Backend
├── MCP stdio client
├── SQLite (trend snapshots)
└── Ollama (local AI brief)
↓
React TS Frontend
└── minimal dashboard UI
```

## Features

- Real GitHub contribution data via GraphQL (includes private repos)
- Local fitness logging with streak tracking
- AI morning brief generated from your actual data — not generic motivation
- Brief cached per day — Ollama only runs once daily unless manually refreshed
- Pluggable MCP server architecture — add your own data sources
- Zero cloud dependencies — everything runs locally

---

## Prerequisites

- Python 3.11+
- Node.js 18+
- [Ollama](https://ollama.ai) running locally with a model pulled (`ollama pull qwen2.5`)
- GitHub Personal Access Token (classic, `read:user` + `repo` scopes)

---

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/yourusername/mcp_dashboard.git
cd mcp_dashboard
```

**2. Configure environment**
```bash
cp .env.example .env
```
Fill in your values in `.env`.

**3. Install dependencies**
```bash
make install
```

**4. Start the dashboard**
```bash
make dev
```

Open `http://localhost:5173`

---

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `GITHUB_TOKEN` | Yes | GitHub PAT (classic), `read:user` + `repo` scopes |
| `GITHUB_USERNAME` | Yes | Your GitHub username |
| `LEETCODE_USERNAME` | Yes | Your LeetCode username |
| `LEETCODE_SESSION_COOKIE` | Yes | LeetCode session cookie from browser |
| `FITNESS_LOG_PATH` | No | Path to fitness JSON (default: `data/fitness.json`) |
| `OLLAMA_HOST` | No | Ollama host (default: `http://localhost:11434`) |
| `OLLAMA_MODEL` | No | Ollama model (default: `qwen2.5:7b`) |

---

## Adding Your Own MCP Server

1. Create a folder in `mcp-servers/your-server/`
2. Implement `server.py` using `FastMCP` with stdio transport
3. Register it in `backend/app/routers/dashboard.py`

Any language that speaks MCP protocol over stdio works.

---

## Project Structure
mcp_dashboard/
├── mcp-servers/        # MCP servers (one per data source)
├── backend/            # FastAPI + MCP client + Ollama
├── frontend/           # React TS dashboard
├── data/               # Local data (gitignored)
├── .env.example        # Config template
└── Makefile            # One-command startup

---

## Roadmap

- [ ] LeetCode MCP server
- [ ] Goals/habits tracking
- [ ] Weekly trend charts
- [ ] Docker Compose support
- [ ] Plugin guide for third-party MCP servers

---

## Stack

Python · FastAPI · MCP Protocol · Ollama · React · TypeScript · SQLite