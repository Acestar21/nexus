.PHONY: install dev backend frontend help

help:
	@echo "Nexus MCP Dashboard"
	@echo ""
	@echo "  make install    Install all dependencies"
	@echo "  make dev        Start backend + frontend"
	@echo "  make backend    Start backend only"
	@echo "  make frontend   Start frontend only"

install:
	pip install -r requirements.txt
	cd frontend && npm install

backend:
	cd backend && uvicorn app.main:app --reload --port 8000

frontend:
	cd frontend && npm run dev

dev:
	@echo "Starting Nexus..."
	@start cmd /k "cd backend && uvicorn app.main:app --reload --port 8000"
	@cd frontend && npm run dev