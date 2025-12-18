"""
AI Service - OpenRouter API Integration
"""

import httpx
import os
from typing import List, Dict, Optional, Any
from config import settings
import time

class AIService:
    """
    Service for calling OpenRouter LLM API
    """
    
    def __init__(self):
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        self.api_key = settings.OPENROUTER_API_KEY
        self.request_count = 0
        self.last_request_time = 0
        self.min_request_interval = 1 / settings.RATE_LIMIT_CALLS  # Rate limiting
    
    async def generate(
        self,
        messages: List[Dict[str, str]],
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 4096
    ) -> Dict[str, Any]:
        """
        Generate response from LLM
        
        Args:
            messages: List of message dicts with role and content
            model: Model to use from OpenRouter
            temperature: Creativity level (0-1)
            max_tokens: Max response length
        
        Returns:
            API response
        """
        # Rate limiting
        await self._rate_limit()
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "https://fabri8.vercel.app",
            "X-Title": "Fabri8 - AI Website Builder"
        }
        
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        try:
            async with httpx.AsyncClient(timeout=120) as client:
                response = await client.post(
                    self.api_url,
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            print(f"API Error: {e}")
            return {
                "error": str(e),
                "choices": [{"message": {"content": "Error generating content"}}]
            }
    
    async def _rate_limit(self):
        """Implement rate limiting"""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_request_interval:
            await asyncio.sleep(self.min_request_interval - elapsed)
        self.last_request_time = time.time()
