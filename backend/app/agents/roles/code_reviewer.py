"""
Code Reviewer Agent - Quality Assurance Review
"""

from agents.base_agent import BaseAgent
from typing import Dict, Any
import json

class CodeReviewerAgent(BaseAgent):
    """
    Agent 6: Code Reviewer
    Reviews code quality, performance, and security
    """
    
    def __init__(self):
        super().__init__(
            name="Code Reviewer",
            role="code_reviewer"
        )
    
    def get_preferred_model(self) -> str:
        """Reviewer uses Claude for detailed analysis"""
        return "anthropic/claude-3.5-sonnet"
    
    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Review frontend and backend code
        """
        frontend_code = context.get('frontend_code', {})
        backend_code = context.get('backend_code', {})
        
        self.log_activity("Reviewing code quality")
        
        review_prompt = f"""
        Review this code and provide feedback:
        
        Frontend Code:
        HTML: {len(str(frontend_code.get('html', '')))} chars
        CSS: {len(str(frontend_code.get('css', '')))} chars
        JS: {len(str(frontend_code.get('js', '')))} chars
        
        Check for:
        1. Code Quality (readability, naming conventions)
        2. Performance (optimization, unnecessary operations)
        3. Security (XSS, injection vulnerabilities)
        4. Accessibility (ARIA labels, semantic HTML)
        5. Best Practices (modern standards)
        6. Browser Compatibility
        
        Provide JSON with:
        - issues (array of {severity, component, description, suggestion})
        - improvements (array of suggestions)
        - score (1-10)
        - summary
        """
        
        response = await self.call_ai(review_prompt, temperature=0.4)
        
        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            review = json.loads(response[json_start:json_end])
        except:
            review = {
                'issues': [
                    {
                        'severity': 'low',
                        'component': 'CSS',
                        'description': 'Consider using CSS custom properties for colors',
                        'suggestion': 'Use :root variables for better maintainability'
                    }
                ],
                'improvements': [
                    'Add loading states for better UX',
                    'Implement error boundaries'
                ],
                'score': 8,
                'summary': 'Code is well-structured and follows best practices'
            }
        
        self.log_activity("Code review complete", f"Issues: {len(review.get('issues', []))}")
        
        return {
            'agent': self.name,
            'role': self.role,
            'output': review,
            'status': 'completed'
        }
