# CodeSage

CodeSage is an AI-powered code review platform designed to automate and enhance the software code review process. It combines traditional static code analysis (Pylint, Bandit, Radon) with Large Language Models (LLMs) to provide meaningful insights into code quality, security, and maintainability.

## Project Vision
To build an intelligent developer assistant that acts as an experienced senior software engineer by automatically reviewing source code, explaining issues clearly, and suggesting actionable improvements.

## Current Status: Phase 1 — Project Skeleton
The project is currently in the **Project Skeleton** phase. We have established the repository structure and initialized the backend and frontend scaffolds.

## Repository Structure
- `backend/`: FastAPI application, dependency management, and analysis logic.
- `frontend/`: Vite + React + Tailwind CSS dashboard.
- `docs/`: Architectural blueprints and design specifications.

## Setup Instructions

### Prerequisites
- Python 3.12+
- Node.js 18+
- [Ollama](https://ollama.com/) (for AI analysis features)

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```
3. Activate the virtual environment:
   - Windows: `.venv\Scripts\activate`
   - Unix/macOS: `source .venv/bin/activate`
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Create a `.env` file based on `.env.example`:
   ```bash
   cp ../.env.example .env
   ```
6. Start the development server:
   ```bash
   python app/main.py
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```

## Development Philosophy
CodeSage is being developed incrementally. Each phase introduces one architectural capability and is considered complete only after engineering review and validation.

## Core Tech Stack
- **Backend:** Python 3.12+, FastAPI
- **Frontend:** React
- **Analysis Engine:** Pylint, Bandit, Radon
- **AI Engine:** Ollama (Local LLM)
- **Database:** PostgreSQL
- **Tooling:** Ruff (Linting & Formatting)

## Engineering Principles
- **Clean Architecture:** Strict separation of concerns between API, Domain, and Infrastructure.
- **Privacy-First:** Local-first analysis with transient source code handling.
- **Hybrid Analysis:** Combining deterministic static analysis with heuristic AI reasoning.
- **Observability:** Built-in request tracing and structured logging.

## Development Roadmap
The project is being built in 15 dependency-driven phases. See the [Project Understanding Document](./PUD.docx) for the full architectural blueprint.

---
*Developed during a software engineering internship as a portfolio-quality learning project.*
