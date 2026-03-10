from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.segnalazioni import router as segnalazioni_router

from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(segnalazioni_router)

@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME}"}


@app.get("/api/health")
async def health_check():
    return {
        "status": "ok",
        "version": settings.PROJECT_VERSION,
    }