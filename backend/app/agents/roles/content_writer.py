"""
Content Writer Agent - Copy & Text
"""

from agents.base_agent import BaseAgent
from typing import Dict, Any
import json

class ContentWriterAgent(BaseAgent):
    """
    Agent 5: Content Writer
    Writes UI copy, descriptions, and text content
    """
    
    def __init__(self):
        super().__init__(
            name="Content Writer",
            role="content_writer"
        )
    
    def get_preferred_model(self) -> str:
        """Writer uses fast Gemini for text generation"""
        return "google/gemini-2.0-flash-exp:free"
    
    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate all copy and content
        """
        project_brief = context.get('project_brief', {})
        design_spec = context.get('design_spec', {})
        
        self.log_activity("Writing content")
        
        content_prompt = f"""
        Write professional, engaging copy for: {project_brief.get('summary', '')}
        
        Provide content for:
        1. Page Title & Meta Description (SEO)
        2. Hero Section (headline, subheading, CTA)
        3. Features Section (feature titles and descriptions)
        4. Call-to-Action Buttons (button labels)
        5. Forms (input labels, placeholders, help text)
        6. Error Messages (user-friendly error texts)
        7. Footer Content (links, copyright info)
        
        Format as JSON with keys:
        - page_title
        - meta_description
        - hero_headline
        - hero_subheading
        - features (array of title + description)
        - buttons (object with label + text)
        - forms (array of field names)
        - error_messages (array)
        - footer_text
        """
        
        response = await self.call_ai(content_prompt, temperature=0.7)
        
        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            content = json.loads(response[json_start:json_end])
        except:
            content = {
                'page_title': project_brief.get('summary', 'Welcome'),
                'meta_description': 'Professional website powered by FABRI8',
                'hero_headline': 'Welcome to our website',
                'hero_subheading': 'We create amazing experiences',
                'features': [
                    {'title': 'Fast', 'description': 'Lightning quick performance'},
                    {'title': 'Secure', 'description': 'Enterprise-grade security'},
                    {'title': 'Scalable', 'description': 'Grows with your business'}
                ],
                'buttons': {'cta': 'Get Started', 'learn_more': 'Learn More'},
                'forms': [{'name': 'Email', 'placeholder': 'your@email.com'}],
                'error_messages': ['Please fill all required fields', 'Invalid email format'],
                'footer_text': '© 2024 FABRI8. All rights reserved.'
            }
        
        self.log_activity("Content written")
        
        return {
            'agent': self.name,
            'role': self.role,
            'output': content,
            'status': 'completed'
        }
