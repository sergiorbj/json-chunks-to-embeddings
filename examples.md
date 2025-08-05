# Exemplos de Uso

Este arquivo contém exemplos práticos de como usar o script com diferentes provedores de IA.

## Configuração Inicial

1. **Copie o arquivo de exemplo:**
```bash
cp env.example .env
```

2. **Configure as chaves de API no arquivo .env:**
```env
# Provedor de IA (openai, gemini, anthropic)
AI_PROVIDER=openai

# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-key-here
OPENAI_EMBEDDING_MODEL=text-embedding-ada-002

# Google Gemini Configuration
GEMINI_API_KEY=your-gemini-api-key-here
GEMINI_EMBEDDING_MODEL=embedding-001

# Anthropic Configuration
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here
ANTHROPIC_EMBEDDING_MODEL=text-embedding-3-small

# Configurações Gerais
BATCH_SIZE=100
```

## Exemplos por Provedor

### 1. OpenAI

**Comando básico:**
```bash
python json_to_embeddings.py sample_input.json --provider openai
```

**Com modelo específico:**
```bash
python json_to_embeddings.py sample_input.json --provider openai --model text-embedding-3-small
```

**Com arquivo de saída personalizado:**
```bash
python json_to_embeddings.py sample_input.json --provider openai -o openai_output.json
```

### 2. Google Gemini

**Comando básico:**
```bash
python json_to_embeddings.py sample_input.json --provider gemini
```

**Com arquivo de saída personalizado:**
```bash
python json_to_embeddings.py sample_input.json --provider gemini -o gemini_output.json
```

### 3. Anthropic

**Comando básico:**
```bash
python json_to_embeddings.py sample_input.json --provider anthropic
```

**Com modelo específico:**
```bash
python json_to_embeddings.py sample_input.json --provider anthropic --model text-embedding-3-large
```

**Com arquivo de saída personalizado:**
```bash
python json_to_embeddings.py sample_input.json --provider anthropic -o anthropic_output.json
```

## Comparação de Provedores

### Teste com o mesmo arquivo de entrada

```bash
# Teste com OpenAI
python json_to_embeddings.py sample_input.json --provider openai -o openai_results.json

# Teste com Gemini
python json_to_embeddings.py sample_input.json --provider gemini -o gemini_results.json

# Teste com Anthropic
python json_to_embeddings.py sample_input.json --provider anthropic -o anthropic_results.json
```

### Comparação de dimensões

Cada provedor gera embeddings com diferentes dimensões:

- **OpenAI**: 1536 (ada-002, 3-small) ou 3072 (3-large)
- **Gemini**: 768 (embedding-001)
- **Anthropic**: 1536 (3-small) ou 3072 (3-large)

## Exemplos Avançados

### Processamento em lotes menores

```bash
python json_to_embeddings.py large_input.json --provider openai --batch-size 25
```

### Usando provedor padrão

Se você configurar `AI_PROVIDER=gemini` no arquivo .env:

```bash
python json_to_embeddings.py sample_input.json
# Usará automaticamente o Gemini
```

### Sobrescrevendo configurações

```bash
# Usar Gemini mesmo com OpenAI configurado como padrão
python json_to_embeddings.py sample_input.json --provider gemini

# Usar modelo específico
python json_to_embeddings.py sample_input.json --provider openai --model text-embedding-3-large
```

## Verificação de Resultados

Após executar o script, você pode verificar os resultados:

```bash
# Verificar estrutura do arquivo de saída
python -c "import json; data=json.load(open('output.json')); print(f'Itens: {len(data)}'); print(f'Dimensões do primeiro embedding: {len(data[0][\"embedding\"])}')"
```

## Troubleshooting

### Erro de API Key

Se você receber um erro sobre API key não encontrada:

1. Verifique se o arquivo `.env` existe
2. Confirme se a chave está correta
3. Verifique se o nome da variável está correto para o provedor

### Erro de modelo

Se você receber um erro sobre modelo não suportado:

1. Verifique a documentação do provedor
2. Use `--list-providers` para ver informações
3. Confirme se o modelo está disponível na sua conta

### Erro de rede

Se você receber erros de conexão:

1. Verifique sua conexão com a internet
2. Confirme se as APIs estão funcionando
3. Verifique se há limites de taxa (rate limits) 