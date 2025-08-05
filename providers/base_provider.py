"""
Abstract base class for AI providers.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any


class BaseProvider(ABC):
    """Abstract base class for embedding providers."""
    
    def __init__(self, api_key: str, model: str):
        """
        Initialize the provider.
        
        Args:
            api_key: Provider API key
            model: Model to be used for embeddings
        """
        self.api_key = api_key
        self.model = model
        self._client = None
    
    @abstractmethod
    def initialize_client(self):
        """Initialize the API client."""
        pass
    
    @abstractmethod
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts.
        
        Args:
            texts: List of texts to generate embeddings for
            
        Returns:
            List of embeddings (each embedding is a list of floats)
        """
        pass
    
    @abstractmethod
    def get_model_info(self) -> Dict[str, Any]:
        """
        Return information about the model.
        
        Returns:
            Dictionary with model information
        """
        pass
    
    def validate_texts(self, texts: List[str]) -> None:
        """
        Validate the list of texts before processing.
        
        Args:
            texts: List of texts to validate
            
        Raises:
            ValueError: If validation fails
        """
        if not texts:
            raise ValueError("Text list cannot be empty")
        
        for i, text in enumerate(texts):
            if not isinstance(text, str):
                raise ValueError(f"Text {i} must be a string")
            if not text.strip():
                raise ValueError(f"Text {i} cannot be empty")
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}(model={self.model})" 