# CodeSage

CodeSage is an AI-powered code review platform designed to automate and enhance the software code review process. It combines traditional static code analysis (Pylint, Bandit, Radon) with Large Language Models (LLMs) to provide meaningful insights into code quality, security, and maintainability.

## Project Vision
To build an intelligent developer assistant that acts as an experienced senior software engineer by automatically reviewing source code, explaining issues clearly, and suggesting actionable improvements.

## Current Status: Phase 0 — Engineering Foundation
The project is currently in the **Engineering Foundation** phase. We are establishing architectural standards, development workflows, and the core system design.

## Repository Structure
This repository will evolve into:
- `backend/`
- `frontend/`
- `docs/`

The structure will be introduced incrementally as development progresses.

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
