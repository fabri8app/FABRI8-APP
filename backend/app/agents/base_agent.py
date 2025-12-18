"""
Base Agent Class - Parent for all agents
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from services.ai_service import AIService
import os

class BaseAgent(ABC):
    """
    Base class for all 8 AI agents
    """
    
    def __init__(self, name: str, role: str):
        """
        Initialize base agent
        
        Args:
            name: Display name of agent
            role: Internal role identifier
        """
        self.name = name
        self.role = role
        self.ai_service = AIService()
        self.system_prompt = self.load_system_prompt()
        self.model = self.get_preferred_model()
    
    def load_system_prompt(self) -> str:
        """
        Load agent-specific system prompt from file
        
        Returns:
            System prompt string
        """
        prompt_file = f"ai/prompts/{self.role}_prompt.txt"
        try:
            with open(prompt_file, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except FileNotFoundError:
            # Fallback prompt
            return f"You are a {self.name}. Perform your role professionally."
    
    @abstractmethod
    def get_preferred_model(self) -> str:
        """
        Return preferred AI model for this agent
        
        Must be implemented by subclasses
        """
        pass
    
    @abstractmethod
    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main execution method
        
        Must be implemented by subclasses
        """
        pass
    
    async def call_ai(
        self,
        user_prompt: str,
        model: Optional[str] = None,
        temperature: float = 0.7
    ) -> str:
        """
        Make AI API call with agent's system prompt
        
        Args:
            user_prompt: The prompt to send to AI
            model: Override default model
            temperature: AI creativity level (0-1)
        
        Returns:
            AI response text
        """
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        response = await self.ai_service.generate(
            messages=messages,
            model=model or self.model,
            temperature=temperature
        )
        
        if response and 'choices' in response:
            return response['choices'][0]['message']['content']
        return ""
    
    def log_activity(self, activity: str, details: str = ""):
        """
        Log agent activity
        """
        print(f"[{self.name}] {activity}")
        if details:
            print(f"  └─ {details}")
