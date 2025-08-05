# Exemplo de Uso - Google Gemini

Este guia mostra como usar o script com foco no Google Gemini para geração de embeddings.

## Configuração Rápida

1. **Copie o arquivo de configuração:**
```bash
cp env.example .env
```

2. **Configure sua chave da API Gemini:**
```bash
# Edite o arquivo .env e adicione sua chave
GEMINI_API_KEY=sua_chave_gemini_aqui
```

3. **Verifique a configuração:**
```bash
python json_to_embeddings.py --list-providers
```

## Uso Básico com Gemini

### Processamento Sem Limite de Batch (Recomendado)

```bash
# Processa todos os itens de uma vez (mais rápido)
python json_to_embeddings.py sample_input.json --provider gemini

# Ou simplesmente (gemini é o padrão)
python json_to_embeddings.py sample_input.json
```

### Processamento com Lotes (Opcional)

```bash
# Se quiser usar lotes específicos
python json_to_embeddings.py sample_input.json --provider gemini --batch-size 50
```

## Vantagens do Gemini

### 1. **Sem Limite de Batch**
- Processa todos os textos de uma vez
- Mais rápido para grandes volumes
- Menos chamadas à API

### 2. **Dimensões Otimizadas**
- 768 dimensões (mais compacto que OpenAI)
- Boa qualidade para a maioria dos casos de uso
- Menor uso de memória

### 3. **Custo Eficiente**
- Preços competitivos
- Sem cobrança por token
- Cobrança por requisição

## Exemplo Completo

### Arquivo de Entrada (input.json)
```json
[
  {
    "content": "A inteligência artificial está revolucionando a forma como trabalhamos.",
    "origin": "artigo_tecnologia"
  },
  {
    "content": "Machine learning permite que computadores aprendam com dados.",
    "origin": "livro_ia"
  },
  {
    "content": "Os embeddings capturam o significado semântico do texto.",
    "origin": "documentacao"
  }
]
```

### Comando de Execução
```bash
python json_to_embeddings.py input.json -o output.json --provider gemini
```

### Arquivo de Saída (output.json)
```json
[
  {
    "content": "A inteligência artificial está revolucionando a forma como trabalhamos.",
    "origin": "artigo_tecnologia",
    "embedding": [0.1, 0.2, 0.3, ...]  // 768 dimensões
  },
  {
    "content": "Machine learning permite que computadores aprendam com dados.",
    "origin": "livro_ia",
    "embedding": [0.4, 0.5, 0.6, ...]  // 768 dimensões
  },
  {
    "content": "Os embeddings capturam o significado semântico do texto.",
    "origin": "documentacao",
    "embedding": [0.7, 0.8, 0.9, ...]  // 768 dimensões
  }
]
```

## Configurações Avançadas

### Variáveis de Ambiente (.env)
```env
# Provedor padrão
AI_PROVIDER=gemini

# Configuração Gemini
GEMINI_API_KEY=sua_chave_aqui
GEMINI_EMBEDDING_MODEL=embedding-001

# Processamento sem limite (recomendado)
BATCH_SIZE=0
```

### Linha de Comando
```bash
# Usar modelo específico
python json_to_embeddings.py input.json --model embedding-001

# Especificar arquivo de saída
python json_to_embeddings.py input.json -o resultado.json

# Combinar opções
python json_to_embeddings.py input.json --provider gemini --model embedding-001 -o output.json
```

## Monitoramento e Logs

O script fornece informações detalhadas durante a execução:

```
Configurações:
  Provedor: gemini
  Modelo: embedding-001
  Tamanho do lote: Sem limite
  Arquivo de entrada: input.json
  Arquivo de saída: output.json

Provedor: Google Gemini
Modelo: embedding-001
Dimensões: 768
Suporte a batch: Sim (sem limite)

Carregando dados de entrada...
Carregados 3 itens

Gerando embeddings...
Processando todos os 3 itens de uma vez...
Embeddings gerados para 3 itens

Salvando resultado...
Dados salvos em: output.json
Processamento concluído com sucesso!
```

## Troubleshooting

### Erro: "API key não encontrada"
```bash
# Verifique se a chave está no arquivo .env
cat .env | grep GEMINI_API_KEY
```

### Erro: "Modelo não suportado"
```bash
# Use o modelo correto
python json_to_embeddings.py input.json --model embedding-001
```

### Performance Lenta
```bash
# Certifique-se de que BATCH_SIZE=0 no .env
# Ou use --batch-size 0 na linha de comando
python json_to_embeddings.py input.json --batch-size 0
```

## Comparação de Performance

| Provedor | Dimensões | Batch Limit | Velocidade |
|----------|-----------|-------------|------------|
| Gemini   | 768       | Sem limite  | ⭐⭐⭐⭐⭐ |
| OpenAI   | 1536      | 100         | ⭐⭐⭐⭐ |
| Anthropic| 1536      | 100         | ⭐⭐⭐⭐ |

## Próximos Passos

1. Configure sua chave da API Gemini
2. Teste com o arquivo `sample_input.json`
3. Processe seus próprios dados
4. Use os embeddings em suas aplicações de IA 