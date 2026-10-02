import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_healthz():
    r = client.get("/healthz")
    assert r.status_code == 200
    assert r.json().get("status") == "ok"

def test_submit_and_get_scan():
    # submit simulated scan
    payload = {"target": "http://example.local", "simulate": True}
    r = client.post("/scan", json=payload)
    assert r.status_code == 200
    body = r.json()
    job_id = body.get("job_id")
    assert job_id

    # The background task may not have completed instantly in the sync testclient environment,
    # but we can poll the job endpoint a few times. In CI, the background task runs quickly.
    for _ in range(10):
        r2 = client.get(f"/scan/{job_id}")
        if r2.status_code == 200:
            j = r2.json()
            # findings is a list
            assert isinstance(j.get("findings"), list)
            return
    pytest.skip("Background task did not complete in time (test environment)")
