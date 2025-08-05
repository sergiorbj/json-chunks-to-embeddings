"""
Google Gemini provider for embedding generation.
"""

import google.generativeai as genai
from typing import List, Dict, Any
from .base_provider import BaseProvider


class GeminiProvider(BaseProvider):
    """Google Gemini provider for embeddings."""
    
    def initialize_client(self):
        """Initialize the Gemini client."""
        genai.configure(api_key=self.api_key)
        self._client = genai
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings using Google Gemini API.
        
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
            
            # Process each text individually (Gemini API limitation)
            for i, text in enumerate(texts):
                print(f"Processing text {i+1}/{len(texts)}: {text[:50]}...")
                
                result = self._client.embed_content(
                    model=self.model,
                    content=text,
                    task_type="retrieval_document"
                )
                
                # Extract embedding from result
                if hasattr(result, 'embedding') and hasattr(result.embedding, 'values'):
                    embeddings.append(result.embedding.values)
                elif isinstance(result, dict) and 'embedding' in result:
                    embeddings.append(result['embedding'])
                else:
                    # Fallback
                    embeddings.append(result.embedding.values)
            
            return embeddings
                
        except Exception as e:
            raise Exception(f"Error generating embeddings with Gemini: {e}")
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Return information about the Gemini model.
        
        Returns:
            Dictionary with model information
        """
        model_info = {
            "provider": "Google Gemini",
            "model": self.model,
            "dimensions": 768,  # Default for embedding models
            "batch_limit": 1,  # Gemini processes one text at a time
            "supports_batch": False
        }
        
        # Adjust dimensions based on model
        if "text-embedding-004" in self.model:
            model_info["dimensions"] = 768
        elif "embedding-001" in self.model:
            model_info["dimensions"] = 768
        
        return model_info 