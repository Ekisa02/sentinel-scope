from fastapi import APIRouter, BackgroundTasks, HTTPException
from uuid import uuid4
from app.schemas.requests import ScanRequest
from app.schemas.responses import ScanResult, Finding
from app.services.pentest_engine import PentestEngine
from app.db.store import InMemoryStore
from app.utils.logging import logger

router = APIRouter()
engine = PentestEngine()
store = InMemoryStore()

@router.post("/scan", response_model=ScanResult)
async def submit_scan(req: ScanRequest, background_tasks: BackgroundTasks):
    # Input validation
    if not req.target:
        raise HTTPException(status_code=400, detail="target is required")

    job_id = str(uuid4())
    logger.info(f"Received scan request {job_id} for target={req.target} simulate={req.simulate}")

    # schedule background job
    background_tasks.add_task(_run_and_store, job_id, req)

    # return an immediate response indicating the job has been accepted with no findings yet
    return ScanResult(job_id=job_id, target=req.target, findings=[])

async def _run_and_store(job_id: str, req: ScanRequest):
    try:
        findings = engine.run_scan(req.target, simulate=bool(req.simulate), notes=req.notes)
        # persist
        store.save(job_id, {
            "job_id": job_id,
            "target": req.target,
            "findings": [f.dict() for f in findings]
        })
        logger.info(f"Scan {job_id} completed with {len(findings)} findings")
    except Exception as exc:
        logger.exception("Error running scan: %s", exc)
        store.save(job_id, {"job_id": job_id, "target": req.target, "error": str(exc)})

@router.get("/scan/{job_id}", response_model=ScanResult)
async def get_scan(job_id: str):
    rec = store.get(job_id)
    if not rec:
        raise HTTPException(status_code=404, detail="job not found")
    if "error" in rec:
        raise HTTPException(status_code=500, detail=rec["error"])
    findings = [Finding(**f) for f in rec.get("findings", [])]
    return ScanResult(job_id=job_id, target=rec.get("target"), findings=findings)
