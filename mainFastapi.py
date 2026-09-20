from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes.trips import router as trips_router


app = FastAPI(
    title="Madinah Tourism AI Agent",
    description="Agentic AI Tourism Planning System",
    version="1.0.0"
)


# Allow frontend (Next.js) to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "message": "Madinah Tourism AI Agent API is running"
    }


@app.get("/api/health")
def health():
    return {
        "status": "healthy"
    }


app.include_router(trips_router)
