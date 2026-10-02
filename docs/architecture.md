# Sentinel Scope Architecture

This document expands on the high-level architecture described in the README.

Components

1. API (FastAPI)
   - Exposes endpoints for submitting scan jobs, checking job status, retrieving findings, and managing models.
   - Uses background tasks for long-running work and a small in-memory store for demonstration.

2. Pentest Engine
   - Runs checks in two modes: simulate (default) and safe-checks (non-exploitative, permission-required).
   - Produces findings as structured objects (type, description, evidence, confidence).

3. ML Model (PyTorch)
   - Lightweight classifier that ingests a numeric feature vector (e.g., heuristic scores) and returns a severity score.
   - Training utilities use synthetic or sanitized datasets to avoid embedding exploit code.

Data flow
- Client -> FastAPI -> pentest_engine.run_scan -> model.predict -> store findings -> client

Security & ethical controls
- Simulation-first approach
- Explicit require_safe flag for any active checks
- Audit logging and storage of operator consent (future)

Scaling notes (future)
- Replace in-memory store with PostgreSQL
- Add a worker queue (Redis + RQ or Celery)
- Model registry and A/B testing for classifiers
