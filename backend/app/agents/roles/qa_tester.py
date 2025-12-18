"""
QA Tester Agent - Testing & Validation
"""

from agents.base_agent import BaseAgent
from typing import Dict, Any
import json

class QATesterAgent(BaseAgent):
    """
    Agent 7: QA Tester
    Creates test plans and validates functionality
    """
    
    def __init__(self):
        super().__init__(
            name="QA Tester",
            role="qa_tester"
        )
    
    def get_preferred_model(self) -> str:
        """QA uses Gemini for test case generation"""
        return "google/gemini-pro"
    
    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate test plans and validation checklist
        """
        project_brief = context.get('project_brief', {})
        
        self.log_activity("Creating test plan")
        
        test_prompt = f"""
        Create comprehensive test plan for: {project_brief.get('summary', '')}
        
        Include:
        1. Happy Path Scenarios (normal user flow)
        2. Edge Cases (boundary conditions)
        3. Error Scenarios (what happens when things go wrong)
        4. Mobile Testing (responsive design)
        5. Performance Testing (load times, etc)
        6. Accessibility Testing
        7. Browser Compatibility
        8. Security Testing
        
        Format as JSON:
        - happy_path (array of test scenarios)
        - edge_cases (array)
        - error_scenarios (array)
        - mobile_tests (array)
        - performance_tests (array)
        - accessibility_tests (array)
        - browser_compatibility (array)
        - security_tests (array)
        """
        
        response = await self.call_ai(test_prompt, temperature=0.5)
        
        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            test_plan = json.loads(response[json_start:json_end])
        except:
            test_plan = {
                'happy_path': [
                    'User lands on homepage',
                    'User navigates to features section',
                    'User clicks CTA button',
                    'Form submission successful'
                ],
                'edge_cases': [
                    'Empty form submission',
                    'Very long input strings',
                    'Special characters in forms'
                ],
                'error_scenarios': ['Network timeout', 'API errors'],
                'mobile_tests': ['iPhone 12', 'Android latest'],
                'performance_tests': ['Page load < 3s', 'First input delay < 100ms'],
                'accessibility_tests': ['Keyboard navigation', 'Screen reader compatibility'],
                'browser_compatibility': ['Chrome', 'Firefox', 'Safari'],
                'security_tests': ['XSS prevention', 'CSRF protection']
            }
        
        self.log_activity("Test plan created", f"Test scenarios: {sum(len(v) if isinstance(v, list) else 1 for v in test_plan.values())}")
        
        return {
            'agent': self.name,
            'role': self.role,
            'output': test_plan,
            'status': 'completed'
        }
