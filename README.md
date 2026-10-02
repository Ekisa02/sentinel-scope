# Sentinel Scope

Sentinel Scope is an ethical, modular automated pentesting framework that combines a FastAPI-based service layer with PyTorch-based machine learning to assist in discovery, triage, and reporting of potential security issues. The project is intended for defensive security teams, education, and research on safe automated assessment techniques.

IMPORTANT: This repository is intentionally designed for safe/ethical use. It contains simulation modes and non-exploitative analysis tools. Do not use it to scan, probe, or attack systems without explicit authorization. Always obtain written permission before running any active tests against third-party systems.

Contents
- Architecture overview
- Installation
- Quickstart (safe demo)
- Project layout
- Development and testing
- Ethical guidance & license

Architecture overview
---------------------
Sentinel Scope is organized into three primary layers:

- API layer (FastAPI): exposes endpoints to submit targets, request scans (simulation by default), and retrieve findings.
- Service / engine layer: orchestrates scan workflows, handles background jobs, and interacts with the model.
- ML model (PyTorch): a small classifier that scores findings to assist triage (severity/priority). The model and training utilities operate on synthetic or curated data; no exploit payloads are embedded.

Sequence (high-level)
1. Client submits a scan request (simulation by default).
2. API triggers the pentest engine to perform safe checks or simulated scans.
3. Engine produces structured findings and consults the ML model to score severity.
4. Findings are stored in a lightweight in-memory store and returned or exported as a report.

Installation
------------
Requirements
- Python 3.9+
- Git

Quick install (recommended: virtual environment)

1. Clone the repository

   git clone https://github.com/your-org/sentinel-scope.git
   cd sentinel-scope

2. Create and activate a virtual environment

   python -m venv .venv
   source .venv/bin/activate  # macOS/Linux
   .\.venv\Scripts\activate  # Windows

3. Install dependencies

   pip install -r requirements.txt

4. Run the API server (development)

   uvicorn app.main:app --reload --port 8000

The API will be available at http://127.0.0.1:8000. Open http://127.0.0.1:8000/docs for interactive API docs (Swagger UI).

Quickstart (safe demo)
----------------------
This demo runs a simulated scan (no network probes). Use the /scan endpoint to submit a target. Example using curl:

curl -X POST "http://127.0.0.1:8000/scan" -H "Content-Type: application/json" -d '{"target": "http://example.local", "simulate": true}'

You will receive structured findings and ML-assisted severity scores.

Project layout
--------------
- app/ - application package (API, services, models, schemas)
  - api/routers/scan.py - API endpoints for scanning
  - core/config.py - central configuration
  - services/pentest_engine.py - orchestrates scan tasks (safe/simulated checks)
  - models/torch_model.py - PyTorch model and inference wrapper
  - schemas/ - request/response pydantic schemas
  - tasks/background.py - background job helpers
- scripts/train_model.py - example training pipeline using synthetic data
- tests/ - pytest-based unit tests (safe, do not perform network attacks)
- docs/architecture.md - extended architecture notes

Development & testing
---------------------
Run tests:

   pytest -q

Run the model training example (generates a small model file in ./models):

   python scripts/train_model.py --epochs 3 --out models/demo_model.pt

Ethical guidance
----------------
Sentinel Scope is for authorized, defensive, and educational use only. Never target systems you do not own or have express permission to test. The default endpoints use simulated scans; active scanning features are gated behind configuration and require explicit operator consent.

License
-------
This project is distributed under the MIT License. See LICENSE for details.

Contributing
------------
Contributions are welcome (issues, PRs). Please follow the code of conduct and include tests for new features. See CONTRIBUTING.md for more information.
