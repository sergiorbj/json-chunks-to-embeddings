#!/usr/bin/env python3
"""
Test script to validate project structure and dependencies.
"""

import json
import sys
from pathlib import Path

def test_json_structure():
    """Test if the sample file has the correct structure"""
    try:
        with open('files/sample_input.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        if not isinstance(data, list):
            print("❌ Error: files/sample_input.json must contain an array")
            return False
        
        for i, item in enumerate(data):
            if not isinstance(item, dict):
                print(f"❌ Error: Item {i} is not a valid object")
                return False
            if 'content' not in item:
                print(f"❌ Error: Item {i} does not have 'content' field")
                return False
            if 'origin' not in item:
                print(f"❌ Error: Item {i} does not have 'origin' field")
                return False
        
        print(f"✅ files/sample_input.json valid with {len(data)} items")
        return True
        
    except Exception as e:
        print(f"❌ Error reading files/sample_input.json: {e}")
        return False

def test_dependencies():
    """Test if dependencies can be imported"""
    try:
        import requests
        print("✅ requests imported successfully")
    except ImportError:
        print("❌ requests not found")
        return False
    
    try:
        import dotenv
        print("✅ python-dotenv imported successfully")
    except ImportError:
        print("❌ python-dotenv not found")
        return False
    
    try:
        import openai
        print("✅ openai imported successfully")
    except ImportError:
        print("❌ openai not found")
        return False
    
    try:
        import google.generativeai
        print("✅ google-generativeai imported successfully")
    except ImportError:
        print("❌ google-generativeai not found")
        return False
    
    try:
        import anthropic
        print("✅ anthropic imported successfully")
    except ImportError:
        print("❌ anthropic not found")
        return False
    
    return True

def test_providers_module():
    """Test if the providers module can be imported"""
    try:
        from providers.provider_factory import ProviderFactory
        print("✅ ProviderFactory imported successfully")
        
        # Test if can list providers
        providers = ProviderFactory.get_supported_providers()
        print(f"✅ Supported providers: {', '.join(providers)}")
        
        return True
    except ImportError as e:
        print(f"❌ Error importing providers module: {e}")
        return False
    except Exception as e:
        print(f"❌ Error testing providers: {e}")
        return False

def test_files_exist():
    """Test if all required files exist"""
    required_files = [
        'json_to_embeddings.py',
        'requirements.txt',
        'env.example',
        'files/sample_input.json',
        'README.md',
        '.gitignore',
        'providers/__init__.py',
        'providers/base_provider.py',
        'providers/provider_factory.py',
        'providers/openai_provider.py',
        'providers/gemini_provider.py',
        'providers/anthropic_provider.py'
    ]
    
    all_exist = True
    for file in required_files:
        if Path(file).exists():
            print(f"✅ {file} exists")
        else:
            print(f"❌ {file} not found")
            all_exist = False
    
    return all_exist

def test_script_help():
    """Test if the main script responds to --help command"""
    try:
        import subprocess
        result = subprocess.run(
            ['python3', 'json_to_embeddings.py', '--help'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0 and 'usage:' in result.stdout:
            print("✅ Main script responds to --help")
            return True
        else:
            print("❌ Main script does not respond correctly to --help")
            return False
    except Exception as e:
        print(f"❌ Error testing main script: {e}")
        return False

def main():
    print("🧪 Running project tests...\n")
    
    tests = [
        ("Checking files", test_files_exist),
        ("Checking dependencies", test_dependencies),
        ("Checking providers module", test_providers_module),
        ("Checking JSON structure", test_json_structure),
        ("Checking main script", test_script_help)
    ]
    
    all_passed = True
    for test_name, test_func in tests:
        print(f"📋 {test_name}:")
        if not test_func():
            all_passed = False
        print()
    
    if all_passed:
        print("🎉 All tests passed!")
        print("\n📝 Next steps:")
        print("1. Copy env.example to .env")
        print("2. Configure desired API keys in .env file")
        print("3. Run: python json_to_embeddings.py --list-providers")
        print("4. Run: python json_to_embeddings.py sample_input.json --provider gemini")
        print("\n💡 Usage examples:")
        print("  # Use Gemini (default)")
        print("  python json_to_embeddings.py input.json --provider gemini")
        print("  # Use OpenAI")
        print("  python json_to_embeddings.py input.json --provider openai")
        print("  # Use Anthropic")
        print("  python json_to_embeddings.py input.json --provider anthropic")
        print("\n📁 Files will be saved to files/ directory")
    else:
        print("❌ Some tests failed. Check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 