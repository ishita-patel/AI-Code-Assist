from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
from pydantic import BaseModel
from enum import Enum
from services.ai_client import generate_code
from database.models import CodeInteraction
from database.database import Base, engine, SessionLocal
from core.config import settings
from chromadb import Client
import logging
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize ChromaDB client
try:
    chroma_client = Client()
    logger.info("ChromaDB client initialized successfully.")
except Exception as e:
    logger.error(f"Error initializing ChromaDB: {e}")
    chroma_client = None

# Initialize FastAPI app
app = FastAPI()

# ✅ Fix CORS issues for frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000", "http://localhost:8000"],  # Explicit origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend static files
app.mount("/static", StaticFiles(directory="Frontend/static"), name="static")

# Serve index.html at root
@app.get("/")
async def serve_index():
    return FileResponse("Frontend/index.html")

# Define supported languages using Enum
class Language(str, Enum):
    PYTHON = "python"
    JAVA = "java"
    JAVASCRIPT = "javascript"
    CPP = "cpp"

# Request model for /generate endpoint
class GenerateRequest(BaseModel):
    prompt: str
    language: Language
    session_id: str

# Dependency for getting DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Background task to store interaction in database
def store_interaction(db: Session, interaction: CodeInteraction):
    try:
        db.add(interaction)
        db.commit()
        logger.info("Interaction stored successfully.")
    except Exception as e:
        db.rollback()
        logger.error(f"Error storing interaction: {e}")

# /generate endpoint for AI-powered code generation
@app.post("/generate")
async def generate_code_endpoint(request: GenerateRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    try:
        logger.info(f"Incoming request: {request}")

        # Call AI model to generate code
        response = generate_code(request.prompt, request.language)
        
        if not response or "code" not in response or "reasoning" not in response:
            logger.error("Invalid response from OpenAI API")
            raise HTTPException(status_code=500, detail="AI response error")

        logger.info(f"Generated code: {response['code']}")

        # Create and store interaction
        interaction = CodeInteraction(
            prompt=request.prompt,
            language=request.language,
            generated_code=response["code"],
            reasoning=response["reasoning"],
            session_id=request.session_id
        )
        background_tasks.add_task(store_interaction, db, interaction)

        return response

    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Catch-all route to serve frontend, but avoid overriding API endpoints
@app.get("/{full_path:path}")
async def catch_all(full_path: str):
    if not full_path.startswith("api/"):
        return FileResponse("Frontend/index.html")
    raise HTTPException(status_code=404, detail="Not Found")
