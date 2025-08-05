#!/usr/bin/env python3
"""
Script to convert text chunks to embeddings using multiple AI providers.
Receives a JSON file with array of objects {content, origin} and adds embeddings.
Special focus on Google Gemini with unlimited batch processing.
"""

import json
import os
import sys
import argparse
from typing import List, Dict, Any
from dotenv import load_dotenv
from providers.provider_factory import ProviderFactory


def load_environment() -> Dict[str, Any]:
    """Loads environment variables from .env file"""
    load_dotenv()
    
    config = {}
    
    # Main provider (default: gemini)
    config['AI_PROVIDER'] = os.getenv('AI_PROVIDER', 'gemini')
    
    # OpenAI Configuration
    config['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
    config['OPENAI_EMBEDDING_MODEL'] = os.getenv('OPENAI_EMBEDDING_MODEL', 'text-embedding-ada-002')
    
    # Gemini Configuration (main focus)
    config['GEMINI_API_KEY'] = os.getenv('GEMINI_API_KEY')
    config['GEMINI_EMBEDDING_MODEL'] = os.getenv('GEMINI_EMBEDDING_MODEL', 'embedding-001')
    
    # Anthropic Configuration
    config['ANTHROPIC_API_KEY'] = os.getenv('ANTHROPIC_API_KEY')
    config['ANTHROPIC_EMBEDDING_MODEL'] = os.getenv('ANTHROPIC_EMBEDDING_MODEL', 'text-embedding-3-small')
    
    # General settings (batch_size optional for Gemini)
    config['BATCH_SIZE'] = int(os.getenv('BATCH_SIZE', '0'))  # 0 = no limit
    
    return config


def load_json_data(file_path: str) -> List[Dict[str, Any]]:
    """Loads JSON data from input file"""
    try:
        # If path doesn't include directory, look in files/
        if not os.path.dirname(file_path):
            file_path = os.path.join('files', file_path)
        
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        if not isinstance(data, list):
            raise ValueError("JSON file must contain an array")
        
        # Validates object structure
        for i, item in enumerate(data):
            if not isinstance(item, dict):
                raise ValueError(f"Item {i} is not a valid object")
            if 'content' not in item:
                raise ValueError(f"Item {i} does not have 'content' field")
            if 'origin' not in item:
                raise ValueError(f"Item {i} does not have 'origin' field")
        
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Error decoding JSON: {e}")


def process_embeddings(provider, data: List[Dict[str, Any]], batch_size: int = 0) -> List[Dict[str, Any]]:
    """Processes embeddings with or without batches depending on provider"""
    model_info = provider.get_model_info()
    
    # For Gemini, process everything at once if batch_size is 0
    if model_info.get('supports_batch') and batch_size == 0:
        print(f"Processing all {len(data)} items at once...")
        
        texts = [item['content'] for item in data]
        embeddings = provider.generate_embeddings(texts)
        
        # Add embeddings to objects
        result = []
        for item, embedding in zip(data, embeddings):
            item_with_embedding = item.copy()
            item_with_embedding['embedding'] = embedding
            result.append(item_with_embedding)
        
        return result
    
    # For other providers or when batch_size > 0, use batch processing
    else:
        if batch_size <= 0:
            batch_size = 100  # Default for other providers
        
        result = []
        for i in range(0, len(data), batch_size):
            batch = data[i:i + batch_size]
            texts = [item['content'] for item in batch]
            
            print(f"Processing batch {i//batch_size + 1}/{(len(data) + batch_size - 1)//batch_size} ({len(texts)} items)")
            
            embeddings = provider.generate_embeddings(texts)
            
            # Add embeddings to objects
            for item, embedding in zip(batch, embeddings):
                item_with_embedding = item.copy()
                item_with_embedding['embedding'] = embedding
                result.append(item_with_embedding)
        
        return result


def save_json_data(data: List[Dict[str, Any]], file_path: str):
    """Saves JSON data to output file"""
    try:
        # Ensure files directory exists
        os.makedirs('files', exist_ok=True)
        
        # If path doesn't include directory, save to files/
        if not os.path.dirname(file_path):
            file_path = os.path.join('files', file_path)
        
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        print(f"Data saved to: {file_path}")
    except Exception as e:
        raise Exception(f"Error saving file: {e}")


def list_providers():
    """Lists all supported providers"""
    providers = ProviderFactory.get_supported_providers()
    print("Supported providers:")
    for provider in providers:
        info = ProviderFactory.get_provider_info(provider)
        print(f"  - {provider}: {info['description']}")
    
    print("\n💡 Tip: For better performance with Gemini, use BATCH_SIZE=0 in .env")


def main():
    parser = argparse.ArgumentParser(description='Convert text chunks to embeddings (focus on Gemini)')
    parser.add_argument('input_file', nargs='?', help='Input JSON file')
    parser.add_argument('-o', '--output', help='Output JSON file (default: output.json)')
    parser.add_argument('--provider', help='AI provider (default: gemini)')
    parser.add_argument('--model', help='Embedding model (overrides provider configuration)')
    parser.add_argument('--batch-size', type=int, help='Batch size (0 = no limit for Gemini)')
    parser.add_argument('--list-providers', action='store_true', help='List supported providers')
    
    args = parser.parse_args()
    
    # If --list-providers was specified, just list providers
    if args.list_providers:
        list_providers()
        return
    
    # Check if input file was provided
    if not args.input_file:
        parser.error("Input file is required (except with --list-providers)")
    
    try:
        # Load configurations
        config = load_environment()
        
        # Use command line arguments if provided
        provider_name = args.provider or config['AI_PROVIDER']
        batch_size = args.batch_size if args.batch_size is not None else config['BATCH_SIZE']
        output_file = args.output or 'output.json'
        
        # Override model if specified
        if args.model:
            config[f'{provider_name.upper()}_EMBEDDING_MODEL'] = args.model
        
        print(f"Configuration:")
        print(f"  Provider: {provider_name}")
        print(f"  Model: {config[f'{provider_name.upper()}_EMBEDDING_MODEL']}")
        print(f"  Batch size: {'No limit' if batch_size == 0 else batch_size}")
        print(f"  Input file: {args.input_file}")
        print(f"  Output file: {output_file}")
        print()
        
        # Create provider
        provider = ProviderFactory.create_provider(provider_name, config)
        model_info = provider.get_model_info()
        
        print(f"Provider: {model_info['provider']}")
        print(f"Model: {model_info['model']}")
        print(f"Dimensions: {model_info['dimensions']}")
        if model_info.get('supports_batch'):
            print(f"Batch support: Yes (no limit)")
        print()
        
        # Load input data
        print("Loading input data...")
        data = load_json_data(args.input_file)
        print(f"Loaded {len(data)} items")
        print()
        
        # Process embeddings
        print("Generating embeddings...")
        result = process_embeddings(provider, data, batch_size)
        print(f"Embeddings generated for {len(result)} items")
        print()
        
        # Save result
        print("Saving result...")
        save_json_data(result, output_file)
        print("Processing completed successfully!")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main() 