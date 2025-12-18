"""
Builder API Routes
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from agents.orchestrator import RealTeamOrchestrator
from services.file_manager import FileManager
import uuid

router = APIRouter()

class GenerateRequest(BaseModel):
    """Request model for website generation"""
    prompt: str
    project_name: Optional[str] = None

class GenerateResponse(BaseModel):
    """Response model for generation"""
    project_id: str
    status: str
    message: str
    code: Optional[dict] = None
    zip_url: Optional[str] = None

@router.post("/generate")
async def generate_website(request: GenerateRequest) -> GenerateResponse:
    """
    Generate complete website from prompt
    
    This triggers the 8-agent, 7-phase workflow
    """
    try:
        # Generate project ID
        project_id = str(uuid.uuid4())
        
        # Initialize orchestrator
        orchestrator = RealTeamOrchestrator(project_id)
        
        # Run workflow
        result = await orchestrator.start_project(request.prompt)
        
        # Save files
        file_manager = FileManager(project_id)
        frontend_code = result.get('frontend_code', {})
        files = file_manager.save_files(frontend_code)
        
        # Save metadata
        file_manager.save_metadata({
            'project_id': project_id,
            'project_name': request.project_name or 'Untitled',
            'prompt': request.prompt,
            'status': 'completed',
            'generated_at': __import__('datetime').datetime.now().isoformat()
        })
        
        # Create ZIP
        zip_bytes = file_manager.create_zip(files)
        
        return GenerateResponse(
            project_id=project_id,
            status='completed',
            message='Website generated successfully!',
            code=frontend_code,
            zip_url=f'/downloads/{project_id}.zip'
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/projects/{project_id}")
async def get_project(project_id: str):
    """Get generated project details"""
    try:
        file_manager = FileManager(project_id)
        with open(f"{file_manager.output_dir}/metadata.json") as f:
            metadata = __import__('json').load(f)
        return metadata
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Project not found")
