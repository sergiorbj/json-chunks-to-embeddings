"""
Anthropic provider for embedding generation.
"""

import anthropic
from typing import List, Dict, Any
from .base_provider import BaseProvider


class AnthropicProvider(BaseProvider):
    """Anthropic provider for embeddings."""
    
    def initialize_client(self):
        """Initialize the Anthropic client."""
        self._client = anthropic.Anthropic(api_key=self.api_key)
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings using Anthropic API.
        
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
            embeddings = []
            for text in texts:
                response = self._client.embeddings.create(
                    model=self.model,
                    input=text
                )
                embeddings.append(response.embedding)
            
            return embeddings
        except Exception as e:
            raise Exception(f"Error generating embeddings with Anthropic: {e}")
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Return information about the Anthropic model.
        
        Returns:
            Dictionary with model information
        """
        model_info = {
            "provider": "Anthropic",
            "model": self.model,
            "dimensions": 1536  # Default for text-embedding-3-small
        }
        
        # Adjust dimensions based on model
        if "text-embedding-3-large" in self.model:
            model_info["dimensions"] = 3072
        elif "text-embedding-3-small" in self.model:
            model_info["dimensions"] = 1536
        
        return model_info 