"""
Frontend Developer Agent - Code Implementation
"""

from agents.base_agent import BaseAgent
from typing import Dict, Any
import re

class FrontendDeveloperAgent(BaseAgent):
    """
    Agent 3: Frontend Developer
    Generates HTML, CSS, JavaScript code
    """
    
    def __init__(self):
        super().__init__(
            name="Frontend Developer",
            role="frontend_dev"
        )
    
    def get_preferred_model(self) -> str:
        """Frontend uses DeepSeek Coder (free & fast)"""
        return "deepseek/deepseek-coder"
    
    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate frontend code
        """
        design_spec = context.get('design_spec', {})
        project_brief = context.get('project_brief', {})
        
        self.log_activity("Generating frontend code")
        
        code_prompt = f"""
        Generate complete modern HTML/CSS/JavaScript code for a website.
        
        Project: {project_brief.get('summary', '')}
        Design Colors: {design_spec.get('colors', {})}
        Components needed: {design_spec.get('components', [])}
        
        Requirements:
        - Responsive design (works on mobile, tablet, desktop)
        - Modern CSS (Flexbox/Grid)
        - Clean, maintainable code
        - No external dependencies (except CDN for icons if needed)
        - Accessibility features (semantic HTML, ARIA labels)
        - Performance optimized
        
        Return EXACTLY in this format:
        ```html
        <!DOCTYPE html>
        ...HTML code...
