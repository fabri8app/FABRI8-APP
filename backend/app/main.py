"""
FastAPI Main Application Entry Point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZIPMiddleware
from fastapi.staticfiles import StaticFiles
import os
from dotenv import load_dotenv
from contextlib import asynccontextmanager

# Load environment variables
load_dotenv()

# Import routes
from routes import auth, projects, builder, agents, websocket

# Lifespan events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 FABRI8 Backend Starting...")
    yield
    # Shutdown
    print("🛑 FABRI8 Backend Shutting Down...")

# Create FastAPI app
app = FastAPI(
    title="FABRI8 API",
    description="AI Website Builder with Multi-Agent Workflow",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:8000",
        "https://fabri8.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# GZIP Middleware
app.add_middleware(GZIPMiddleware, minimum_size=1000)

# Routes
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(projects.router, prefix="/api/projects", tags=["Projects"])
app.include_router(builder.router, prefix="/api/builder", tags=["Builder"])
app.include_router(agents.router, prefix="/api/agents", tags=["Agents"])
app.include_router(websocket.router)

# Root endpoint
@app.get("/", tags=["Health"])
async def root():
    """Root endpoint - Health check"""
    return {
        "status": "ok",
        "app": "FABRI8 Backend",
        "version": "1.0.0",
        "message": "AI Website Builder API"
    }

# Health check endpoint
@app.get("/health", tags=["Health"])
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "fabri8-backend",
        "timestamp": __import__("datetime").datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=os.getenv("SERVER_HOST", "0.0.0.0"),
        port=int(os.getenv("SERVER_PORT", 8000)),
        reload=os.getenv("DEBUG", True)
    )
