from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routers import appointments, auth, availability, professionals, services

app = FastAPI(
    title="TECHNOVINHO API",
    description="Gestão de barbearias — APS GTIADS 2026.1",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(services.router)
app.include_router(professionals.router)
app.include_router(appointments.router)
app.include_router(availability.router)


@app.get("/")
def root():
    return {"message": "API TECHNOVINHO está no ar"}


@app.get("/api/health")
def health():
    return {"status": "ok"}
