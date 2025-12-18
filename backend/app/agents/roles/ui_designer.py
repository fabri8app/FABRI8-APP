"""
UI/UX Designer Agent - Design Phase
"""

from agents.base_agent import BaseAgent
from typing import Dict, Any
import json

class UIDesignerAgent(BaseAgent):
    """
    Agent 2: UI/UX Designer
    Creates design specifications and visual guidelines
    """
    
    def __init__(self):
        super().__init__(
            name="UI/UX Designer",
            role="ui_designer"
        )
    
    def get_preferred_model(self) -> str:
        """Designer uses GPT-4o for visual creativity"""
        return "openai/gpt-4o"
    
    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create design specifications
        """
        project_brief = context.get('project_brief', {})
        
        self.log_activity("Creating design concepts")
        
        design_prompt = f"""
        Project: {project_brief.get('summary', '')}
        Design Direction: {project_brief.get('design_direction', '')}
        Target Users: {project_brief.get('target_users', '')}
        
        Create a comprehensive design specification:
        1. Layout Strategy (grid, sections, flow)
        2. Color Palette (primary, secondary, accent colors - hex codes)
        3. Typography (fonts, sizes, weights)
        4. Component List (header, buttons, cards, forms, etc)
        5. Responsive Breakpoints (mobile, tablet, desktop dimensions)
        6. Visual Hierarchy
        7. Accessibility Considerations
        
        Format as JSON with keys:
        - layout
        - colors (object with primary, secondary, accent)
        - typography (object with font_family, sizes)
        - components (array)
        - breakpoints (object)
        - visual_hierarchy
        - accessibility_notes
        """
        
        response = await self.call_ai(design_prompt, temperature=0.8)
        
        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            design_spec = json.loads(response[json_start:json_end])
        except:
            design_spec = {
                'layout': 'Hero section + Features + Footer',
                'colors': {
                    'primary': '#3498db',
                    'secondary': '#2c3e50',
                    'accent': '#e74c3c'
                },
                'typography': {
                    'font_family': 'Inter, sans-serif',
                    'sizes': ['12px', '14px', '16px', '24px', '32px']
                },
                'components': ['Header', 'Hero', 'Features', 'CTA', 'Footer'],
                'breakpoints': {'mobile': '320px', 'tablet': '768px', 'desktop': '1024px'},
                'visual_hierarchy': 'Bold headers, subtle backgrounds',
                'accessibility_notes': 'WCAG 2.1 AA compliant'
            }
        
        self.log_activity("Design created", f"Components: {len(design_spec.get('components', []))}")
        
        return {
            'agent': self.name,
            'role': self.role,
            'output': design_spec,
            'status': 'completed'
        }
