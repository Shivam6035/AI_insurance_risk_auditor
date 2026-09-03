

# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.staticfiles import StaticFiles
# from fastapi.responses import FileResponse
# from pathlib import Path

# from app.api.routes import router as api_router
# from app.core.exceptions import register_exception_handlers
# from app.core.config import settings

# app = FastAPI(title=settings.PROJECT_NAME)

# # 1. Middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # 2. Exception Handlers
# register_exception_handlers(app)

# # 3. API Routes (Must be loaded BEFORE frontend routes)
# app.include_router(api_router, prefix="/api/v1")

# # 4. Health Check (Must be loaded BEFORE catch-all frontend routes)
# @app.get("/health", tags=["Health"])
# async def health_check():
#     return {"status": "healthy", "service": "insurance-auditor"}

# # 5. Static Files Mounting
# frontend_dir = Path(__file__).resolve().parent.parent / "frontend"
# app.mount("/css", StaticFiles(directory=frontend_dir / "css"), name="css")
# app.mount("/js", StaticFiles(directory=frontend_dir / "js"), name="js")

# # # 6. Frontend Routes
# # @app.get("/compare", include_in_schema=False)
# # async def serve_compare():
# #     return FileResponse(frontend_dir / "compare.html")

# # @app.get("/", include_in_schema=False)
# # async def serve_index():
# #     return FileResponse(frontend_dir / "index.html")


# # 6. Frontend Routes
# @app.get("/compare", include_in_schema=False)
# async def serve_compare():
#     return FileResponse(frontend_dir / "compare.html")

# @app.get("/", include_in_schema=False)
# async def serve_index():
#     return FileResponse(frontend_dir / "index.html")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

from app.api.routes import router as api_router
from app.core.exceptions import register_exception_handlers
from app.core.config import settings


app = FastAPI(title=settings.PROJECT_NAME)

# 1. Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Exception Handlers
register_exception_handlers(app)

# 3. API Routes
app.include_router(api_router, prefix="/api/v1")

# 4. Health Check
@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "service": "insurance-auditor"
    }


# 5. Frontend paths
frontend_dir = Path(__file__).resolve().parent.parent / "frontend"
css_dir = frontend_dir / "css"
js_dir = frontend_dir / "js"

# Railway/Git may not preserve empty directories.
# Make sure they exist before StaticFiles checks them.
css_dir.mkdir(parents=True, exist_ok=True)
js_dir.mkdir(parents=True, exist_ok=True)


# 6. Static Files
app.mount(
    "/css",
    StaticFiles(directory=str(css_dir)),
    name="css",
)

app.mount(
    "/js",
    StaticFiles(directory=str(js_dir)),
    name="js",
)


# 7. Frontend Routes
@app.get("/compare", include_in_schema=False)
async def serve_compare():
    return FileResponse(frontend_dir / "compare.html")


@app.get("/", include_in_schema=False)
async def serve_index():
    return FileResponse(frontend_dir / "index.html")