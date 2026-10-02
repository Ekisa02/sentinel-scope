from typing import Dict, Any


class InMemoryStore:
    def __init__(self):
        self._store: Dict[str, Any] = {}

    def save(self, job_id: str, payload: Dict[str, Any]):
        self._store[job_id] = payload

    def get(self, job_id: str):
        return self._store.get(job_id)
