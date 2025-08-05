"""
OpenAI provider for embedding generation.
"""

from typing import List, Dict, Any
from openai import OpenAI
from .base_provider import BaseProvider


class OpenAIProvider(BaseProvider):
    """OpenAI provider for embeddings."""
    
    def initialize_client(self):
        """Initialize the OpenAI client."""
        self._client = OpenAI(api_key=self.api_key)
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings using OpenAI API.
        
        Args:
            texts: List of texts to generate embeddings for
            
        Returns:
            List of embeddings
            
        Raises:
            Exception: If there's an API error
        """
        self.validate_texts(texts)
        
        if not self._client:
            self.initialize_client()
        
        try:
            response = self._client.embeddings.create(
                model=self.model,
                input=texts
            )
            return [embedding.embedding for embedding in response.data]
        except Exception as e:
            raise Exception(f"Error generating embeddings with OpenAI: {e}")
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Return information about the OpenAI model.
        
        Returns:
            Dictionary with model information
        """
        model_info = {
            "provider": "OpenAI",
            "model": self.model,
            "dimensions": 1536  # Default for text-embedding-ada-002
        }
        
        # Adjust dimensions based on model
        if "text-embedding-3-large" in self.model:
            model_info["dimensions"] = 3072
        elif "text-embedding-3-small" in self.model:
            model_info["dimensions"] = 1536
        elif "text-embedding-ada-002" in self.model:
            model_info["dimensions"] = 1536
        
        return model_info 