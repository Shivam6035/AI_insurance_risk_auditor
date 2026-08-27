# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from app.api.routes import router
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.staticfiles import StaticFiles
# from fastapi.responses import FileResponse
# from pathlib import Path

# from app.api.routes import router as api_router
# from app.core.exceptions import register_exception_handlers
# from app.core.config import settings

# # Initialize the FastAPI application
# app = FastAPI(
#     title="AI Insurance Policy Auditor",
#     description="An Agentic RAG system that calculates health scores for insurance policies.",
#     version="1.0.0"
# )

# # Configure CORS to allow frontend connections
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # In production, replace "*" with your frontend URL (e.g., "https://myapp.com")
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Mount the routes
# app.include_router(router)

# @app.get("/health")
# def health_check():
#     """Simple endpoint to verify the server is running."""
#     return {"status": "healthy", "service": "insurance-auditor"}

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

from app.api.routes import router as api_router
from app.core.exceptions import register_exception_handlers
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

# 1. Enable CORS for frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Register custom exception handlers
register_exception_handlers(app)

# 3. Include API routes
app.include_router(api_router, prefix=settings.API_V1_STR)

# 4. Mount frontend static assets (CSS, JS)
frontend_dir = Path(__file__).resolve().parent.parent / "frontend"
app.mount("/css", StaticFiles(directory=frontend_dir / "css"), name="css")
app.mount("/js", StaticFiles(directory=frontend_dir / "js"), name="js")

# 5. Serve index.html on root GET /
@app.get("/", include_in_schema=False)
async def serve_index():
    return FileResponse(frontend_dir / "index.html")

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy", "service": "insurance-auditor"}

    