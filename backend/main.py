from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.config import settings

# Initialize the FastAPI application instance
app = FastAPI(
    title="Synapse API",
    description="Backend API for Synapse: Cognitive Ergonomics & Systems Learning PWA",
    version="1.0.0"
)

# Configure CORS (Cross-Origin Resource Sharing) middleware
# This ensures your front-end (running locally on Vite/live-server or PWA clients) can communicate securely with the backend.
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Health Check"])
def read_root():
    """
    Root health check endpoint to confirm the Synapse backend is up and running.
    """
    return {
        "status": "online",
        "app": "Synapse API",
        "version": "1.0.0"
    }