# JSON Chunks to Embeddings

Python script to convert text chunks to embeddings using multiple AI providers, with **special focus on Google Gemini** for maximum performance.

## 🚀 Features

- **🎯 Gemini Focus**: Default provider optimized for performance
- **⚡ No Batch Limit**: Processes all texts at once (Gemini)
- **🔧 Multiple Providers**: Support for OpenAI, Google Gemini and Anthropic
- **🏗️ Modular Architecture**: Easy addition of new providers
- **⚙️ Flexible Configuration**: Via environment variables or command line
- **✅ Robust Validation**: Input verification and error handling

## 📁 File Structure

```
json-chunks-to-embeddings/
├── files/                    # Input and output files directory
│   ├── sample_input.json    # Sample input file
│   └── output.json          # Generated output (after processing)
├── providers/               # AI providers module
├── json_to_embeddings.py   # Main script
├── requirements.txt         # Dependencies
├── env.example             # Environment configuration template
└── README.md               # Documentation
```

## 📁 Input Structure

The input JSON file must contain an array of objects with the following structure:

```json
[
  {
    "content": "Text to be converted to embedding",
    "origin": "Origin or chunk identifier"
  }
]
```

## 📤 Output Structure

The output JSON file will maintain the original structure and add the `embedding` field:

```json
[
  {
    "content": "Text to be converted to embedding",
    "origin": "Origin or chunk identifier",
    "embedding": [0.1, 0.2, 0.3, ...]  // 768 dimensions (Gemini)
  }
]
```

## 🛠️ Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd json-chunks-to-embeddings
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp env.example .env
```

4. Edit the `.env` file with your configurations:
```env
# AI Provider (default: gemini)
AI_PROVIDER=gemini

# Google Gemini Configuration (RECOMMENDED)
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_EMBEDDING_MODEL=embedding-001

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_EMBEDDING_MODEL=text-embedding-ada-002

# Anthropic Configuration
ANTHROPIC_API_KEY=your_anthropic_api_key_here
ANTHROPIC_EMBEDDING_MODEL=text-embedding-3-small

# General Settings
# For Gemini: 0 = no batch limit (recommended)
# For other providers: batch size (e.g., 100)
BATCH_SIZE=0
```

## 🚀 Usage

### List Supported Providers

```bash
python json_to_embeddings.py --list-providers
```

### Basic Usage with Gemini (Recommended)

```bash
# Process all items at once (faster)
python json_to_embeddings.py input.json --provider gemini

# Or simply (gemini is default)
python json_to_embeddings.py input.json
```

### Usage with Other Providers

```bash
# OpenAI
python json_to_embeddings.py input.json --provider openai

# Anthropic
python json_to_embeddings.py input.json --provider anthropic
```

### Advanced Options

```bash
# Specify output file
python json_to_embeddings.py input.json -o output.json

# Use specific model
python json_to_embeddings.py input.json --model embedding-001

# Set batch size (for other providers)
python json_to_embeddings.py input.json --batch-size 50

# Combine options
python json_to_embeddings.py input.json -o result.json --provider gemini --model embedding-001
```

### Example with Test File

```bash
python json_to_embeddings.py sample_input.json -o sample_output.json --provider gemini
```

*Note: Input and output files are automatically managed in the `files/` directory*

## 🎯 Supported Providers

### Google Gemini ⭐ (Recommended)
- **Models**: `embedding-001`
- **Dimensions**: 768
- **Advantages**: No batch limit, faster, cost efficient
- **Configuration**: `GEMINI_API_KEY`, `GEMINI_EMBEDDING_MODEL`

### OpenAI
- **Models**: `text-embedding-ada-002`, `text-embedding-3-small`, `text-embedding-3-large`
- **Dimensions**: 1536 (ada-002, 3-small) or 3072 (3-large)
- **Configuration**: `OPENAI_API_KEY`, `OPENAI_EMBEDDING_MODEL`

### Anthropic
- **Models**: `text-embedding-3-small`, `text-embedding-3-large`
- **Dimensions**: 1536 (small) or 3072 (large)
- **Configuration**: `ANTHROPIC_API_KEY`, `ANTHROPIC_EMBEDDING_MODEL`

## ⚙️ Configuration

### Environment Variables

- `AI_PROVIDER`: Default provider (default: gemini)
- `BATCH_SIZE`: Batch size (0 = no limit for Gemini)

### Provider Configurations

Each provider has its own configuration variables:

- **Gemini**: `GEMINI_API_KEY`, `GEMINI_EMBEDDING_MODEL`
- **OpenAI**: `OPENAI_API_KEY`, `OPENAI_EMBEDDING_MODEL`
- **Anthropic**: `ANTHROPIC_API_KEY`, `ANTHROPIC_EMBEDDING_MODEL`

### Adding New Providers

To add a new provider:

1. Create a new class that inherits from `BaseProvider`
2. Implement required methods
3. Add provider to `ProviderFactory`
4. Update environment configurations

## ⚡ Performance

- **Gemini**: Unlimited batch processing for maximum speed
- **Other Providers**: Optimized batch processing
- Progress bar during processing
- Informative logs about progress
- Support for different embedding dimensions

## 📋 Requirements

- Python 3.7+
- Google AI Studio account (for Gemini) or other providers

## 🧪 Testing

Run the test script to verify everything is working:

```bash
python test_script.py
```