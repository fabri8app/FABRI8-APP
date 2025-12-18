"""
Project Manager Agent - Phase 1 Discovery
"""

from agents.base_agent import BaseAgent
from typing import Dict, Any
import json

class ProjectManagerAgent(BaseAgent):
    """
    Agent 1: Project Manager
    Analyzes requirements and creates detailed PRD
    """
    
    def __init__(self):
        super().__init__(
            name="Project Manager",
            role="project_manager"
        )
    
    def get_preferred_model(self) -> str:
        """PM uses Claude for deep analysis"""
        return "anthropic/claude-3.5-sonnet"
    
    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze user prompt and create project brief
        """
        user_prompt = context.get('prompt', '')
        
        self.log_activity("Starting analysis", f"Prompt length: {len(user_prompt)} chars")
        
        analysis_prompt = f"""
        User Request: {user_prompt}
        
        Analyze this request and provide:
        1. Project Summary (1-2 lines)
        2. Target Users (who will use this)
        3. Key Features (5-10 main features)
        4. Technical Requirements
        5. Design Direction (modern, minimal, colorful, etc)
        6. Timeline Estimate
        7. Success Metrics
        
        Format as JSON with these exact keys:
        - summary
        - target_users
        - key_features (array)
        - technical_requirements
        - design_direction
        - timeline_estimate
        - success_metrics (array)
        """
        
        response = await self.call_ai(analysis_prompt, temperature=0.5)
        
        try:
            # Extract JSON from response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            analysis_json = json.loads(response[json_start:json_end])
        except:
            # Fallback if JSON parsing fails
            analysis_json = {
                'summary': user_prompt[:100],
                'target_users': 'General users',
                'key_features': ['Core Feature 1', 'Core Feature 2', 'Core Feature 3'],
                'technical_requirements': 'Modern web standards',
                'design_direction': 'Modern and clean',
                'timeline_estimate': '2-4 hours',
                'success_metrics': ['Functional', 'Responsive', 'Fast']
            }
        
        self.log_activity("Analysis complete", f"Features identified: {len(analysis_json.get('key_features', []))}")
        
        return {
            'agent': self.name,
            'role': self.role,
            'output': analysis_json,
            'status': 'completed'
        }
