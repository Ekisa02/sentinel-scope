from fastapi import FastAPI
from app.api.routers.scan import router as scan_router
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

app.include_router(scan_router, prefix="", tags=["scan"])

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}
