from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union

class BaseLLM(ABC):
    """Abstract base class for LLM providers."""
    
    @abstractmethod
    async def generate(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate a response from the LLM."""
        pass

    @abstractmethod
    def get_model_info(self) -> Dict[str, str]:
        """Return information about the model."""
        pass
