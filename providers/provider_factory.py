"""
AI provider factory.
"""

from typing import Dict, Any
from .base_provider import BaseProvider
from .openai_provider import OpenAIProvider
from .gemini_provider import GeminiProvider
from .anthropic_provider import AnthropicProvider


class ProviderFactory:
    """Factory for creating AI provider instances."""
    
    _providers = {
        'openai': OpenAIProvider,
        'gemini': GeminiProvider,
        'anthropic': AnthropicProvider
    }
    
    @classmethod
    def create_provider(cls, provider_name: str, config: Dict[str, Any]) -> BaseProvider:
        """
        Create an instance of the specified provider.
        
        Args:
            provider_name: Provider name (openai, gemini, anthropic)
            config: Provider configuration
            
        Returns:
            Provider instance
            
        Raises:
            ValueError: If provider is not supported
        """
        provider_name = provider_name.lower()
        
        if provider_name not in cls._providers:
            supported = ', '.join(cls._providers.keys())
            raise ValueError(f"Provider '{provider_name}' not supported. Supported providers: {supported}")
        
        provider_class = cls._providers[provider_name]
        
        # Extract provider-specific configurations
        api_key = config.get(f'{provider_name.upper()}_API_KEY')
        model = config.get(f'{provider_name.upper()}_EMBEDDING_MODEL')
        
        if not api_key:
            raise ValueError(f"API key for {provider_name} not found in configuration")
        
        if not model:
            raise ValueError(f"Model for {provider_name} not found in configuration")
        
        return provider_class(api_key=api_key, model=model)
    
    @classmethod
    def get_supported_providers(cls) -> list:
        """
        Return list of supported providers.
        
        Returns:
            List of supported provider names
        """
        return list(cls._providers.keys())
    
    @classmethod
    def get_provider_info(cls, provider_name: str) -> Dict[str, Any]:
        """
        Return information about a specific provider.
        
        Args:
            provider_name: Provider name
            
        Returns:
            Dictionary with provider information
        """
        provider_name = provider_name.lower()
        
        if provider_name not in cls._providers:
            return {"error": f"Provider '{provider_name}' not supported"}
        
        provider_class = cls._providers[provider_name]
        
        return {
            "name": provider_name,
            "class": provider_class.__name__,
            "module": provider_class.__module__,
            "description": provider_class.__doc__ or "No description available"
        } 