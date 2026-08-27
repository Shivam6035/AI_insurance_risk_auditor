from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router

# Initialize the FastAPI application
app = FastAPI(
    title="AI Insurance Policy Auditor",
    description="An Agentic RAG system that calculates health scores for insurance policies.",
    version="1.0.0"
)

# Configure CORS to allow frontend connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace "*" with your frontend URL (e.g., "https://myapp.com")
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the routes
app.include_router(router)

@app.get("/health")
def health_check():
    """Simple endpoint to verify the server is running."""
    return {"status": "healthy", "service": "insurance-auditor"}