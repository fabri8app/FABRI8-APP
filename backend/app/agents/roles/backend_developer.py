"""
Backend Developer Agent - API Implementation
"""

from agents.base_agent import BaseAgent
from typing import Dict, Any
import json

class BackendDeveloperAgent(BaseAgent):
    """
    Agent 4: Backend Developer
    Generates API routes and backend logic
    """
    
    def __init__(self):
        super().__init__(
            name="Backend Developer",
            role="backend_dev"
        )
    
    def get_preferred_model(self) -> str:
        """Backend uses DeepSeek Coder (free & specialized for code)"""
        return "deepseek/deepseek-coder"
    
    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate backend code/API documentation
        """
        project_brief = context.get('project_brief', {})
        
        self.log_activity("Designing backend architecture")
        
        backend_prompt = f"""
        Design backend architecture for: {project_brief.get('summary', '')}
        
        Provide:
        1. Database Models (tables, fields, relationships)
        2. API Endpoints (HTTP methods, paths, parameters, responses)
        3. Authentication Strategy
        4. Error Handling
        5. Validation Rules
        
        Format as JSON with keys:
        - database_models (array of objects with name, fields)
        - api_endpoints (array with method, path, description, params, response)
        - authentication (strategy description)
        - error_handling (standard error codes)
        - validation_rules (array of rules)
        """
        
        response = await self.call_ai(backend_prompt, temperature=0.5)
        
        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            backend_design = json.loads(response[json_start:json_end])
        except:
            backend_design = {
                'database_models': [
                    {'name': 'User', 'fields': ['id', 'email', 'name', 'created_at']},
                    {'name': 'Project', 'fields': ['id', 'user_id', 'title', 'description']}
                ],
                'api_endpoints': [
                    {
                        'method': 'GET',
                        'path': '/api/projects',
                        'description': 'Get all projects',
                        'response': {'projects': []}
                    }
                ],
                'authentication': 'JWT tokens',
                'error_handling': 'RESTful error codes (400, 401, 404, 500)',
                'validation_rules': ['Email validation', 'Required fields check']
            }
        
        self.log_activity("Backend designed", f"Endpoints: {len(backend_design.get('api_endpoints', []))}")
        
        return {
            'agent': self.name,
            'role': self.role,
            'output': backend_design,
            'status': 'completed'
        }
