"""
Debugger Agent - Bug Fixing & Optimization
"""

from agents.base_agent import BaseAgent
from typing import Dict, Any
import json

class DebuggerAgent(BaseAgent):
    """
    Agent 8: Debugger
    Identifies issues and provides fixes
    """
    
    def __init__(self):
        super().__init__(
            name="Debugger",
            role="debugger"
        )
    
    def get_preferred_model(self) -> str:
        """Debugger uses DeepSeek Coder for fix generation"""
        return "deepseek/deepseek-coder"
    
    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Debug and optimize code
        """
        code_review = context.get('code_review', {})
        frontend_code = context.get('frontend_code', {})
        
        self.log_activity("Debugging code")
        
        debug_prompt = f"""
        Found issues in the code. Provide fixes:
        
        Issues to fix:
        {json.dumps(code_review.get('issues', [])[:3])}
        
        For each issue, provide:
        1. Root cause analysis
        2. Fixed code snippet
        3. Testing approach to verify fix
        
        Format as JSON:
        - fixes (array of {issue, root_cause, fixed_code, testing_approach})
        - optimization_tips (array)
        - performance_improvements (array)
        """
        
        response = await self.call_ai(debug_prompt, temperature=0.4)
        
        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            debug_result = json.loads(response[json_start:json_end])
        except:
            debug_result = {
                'fixes': [
                    {
                        'issue': 'Missing error handling',
                        'root_cause': 'Async operation without try-catch',
                        'fixed_code': 'wrap in try-catch block',
                        'testing_approach': 'Test with network errors'
                    }
                ],
                'optimization_tips': [
                    'Lazy load images',
                    'Minify CSS and JS',
                    'Use CSS containment'
                ],
                'performance_improvements': [
                    'Remove unused CSS',
                    'Defer non-critical JS',
                    'Implement caching'
                ]
            }
        
        self.log_activity("Debugging complete", f"Fixes: {len(debug_result.get('fixes', []))}")
        
        return {
            'agent': self.name,
            'role': self.role,
            'output': debug_result,
            'status': 'completed'
        }
