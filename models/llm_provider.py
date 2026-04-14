import os
from typing import Any, Dict
import google.generativeai as genai
from .base import BaseLLM
from loguru import logger

class MockLLM(BaseLLM):
    """Mock LLM for testing and local development."""
    async def generate(self, prompt: str, **kwargs) -> Dict[str, Any]:
        logger.info(f"Mocking response for prompt: {prompt[:50]}...")
        return {
            "text": "This is a mock response from the LLM service.",
            "usage": {"prompt_tokens": 10, "completion_tokens": 10, "total_tokens": 20},
            "model": "mock-llm-v1"
        }

    def get_model_info(self) -> Dict[str, str]:
        return {"name": "MockLLM", "version": "1.0.0"}

from tenacity import retry, stop_after_attempt, wait_exponential

class GeminiLLM(BaseLLM):
    """Google Gemini LLM implementation with built-in retries."""
    def __init__(self, api_key: str, model_name: str = "gemini-1.5-flash"):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        self.model_name = model_name

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True
    )
    async def generate(self, prompt: str, **kwargs) -> Dict[str, Any]:
        try:
            response = await self.model.generate_content_async(prompt)
            return {
                "text": response.text,
                "usage": {"total_tokens": None},
                "model": self.model_name
            }
        except Exception as e:
            logger.error(f"Gemini API Error (retrying...): {str(e)}")
            raise e

    def get_model_info(self) -> Dict[str, str]:
        return {"name": "GeminiLLM", "version": self.model_name}

def get_llm_provider(provider_type: str = "mock", **kwargs) -> BaseLLM:
    """Factory function to get LLM provider."""
    if provider_type == "gemini":
        return GeminiLLM(api_key=kwargs.get("api_key"), model_name=kwargs.get("model_name", "gemini-1.5-flash"))
    return MockLLM()
