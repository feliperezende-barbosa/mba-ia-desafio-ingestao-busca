# Projeto de Ingestão e Busca com IA

Este projeto consiste em um sistema de ingestão de documentos PDF e uma interface de chat para realizar perguntas sobre o conteúdo dos documentos, utilizando modelos de linguagem (LLMs) e armazenamento vetorial.

## Tecnologias Utilizadas

- **Python 3.11+**
- **Docker e Docker Compose**
- **PostgreSQL com pgvector:** Banco de dados para armazenamento vetorial dos embeddings.
- **LangChain:** Framework para desenvolvimento de aplicações com LLMs.
- **LLMs Suportados:**
  - OpenAI (Padrão)
  - Google Gemini
  - Azure OpenAI
- **Bibliotecas Python:** `pypdf` para leitura de PDFs, `langchain-postgres` para integração com pgvector, entre outras listadas no `requirements.txt`.

## Estrutura do Projeto

```
.
├── docker-compose.yml      # Orquestração dos contêineres Docker (PostgreSQL)
├── README.md               # Documentação do projeto
├── requirements.txt        # Dependências Python
├── .env.example            # Exemplo de arquivo de variáveis de ambiente
├── src
│   ├── chat.py             # Lógica do chat interativo com o LLM
│   ├── embeddings.py       # Geração de embeddings a partir do texto
│   ├── ingest.py           # Ingestão do documento PDF para o banco vetorial
│   ├── llm.py              # Configuração e inicialização do modelo de linguagem
│   ├── search.py           # Lógica de busca e recuperação de informações no banco vetorial
│   └── settings.py         # Configurações da aplicação e variáveis de ambiente
└── document.pdf            # Documento a ser ingerido (coloque seu PDF aqui)
```

## Pré-requisitos

- **Docker e Docker Compose:** Para executar o banco de dados PostgreSQL com a extensão `pgvector`.
- **Python 3.11+ e pip:** Para gerenciar as dependências e executar os scripts.
- **Chave de API de um provedor de LLM:** (OpenAI, Google ou Azure).

## Como Executar

### 1. Configuração do Ambiente

Clone o repositório e navegue para a pasta do projeto.

**a. Variáveis de Ambiente:**

Crie um arquivo `.env` na raiz do projeto, copiando o conteúdo de `.env.example`.

```bash
cp .env.example .env
```

Edite o arquivo `.env` e preencha as variáveis de acordo com o provedor de LLM escolhido.

**Exemplo para OpenAI:**
```env
# Configurações do Banco de Dados
DATABASE_URL="postgresql+psycopg2://postgres:postgres@localhost:5432/rag"
PG_VECTOR_COLLECTION_NAME="my_collection"
PDF_PATH="document.pdf"

# Handler do LangChain (openai, azure, google)
LANGCHAIN_HANDLER="openai"

# --- Configurações para OpenAI ---
OPENAI_API_KEY="sua-chave-de-api-aqui"
OPENAI_EMBEDDING_MODEL="text-embedding-3-small"
OPENAI_LLM_MODEL="gpt-4o"
```

**b. Instalação das Dependências:**

Crie um ambiente virtual e instale as dependências:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Subir o Banco de Dados

Com o Docker em execução, inicie o contêiner do PostgreSQL:

```bash
docker-compose up -d
```

Este comando irá:
1. Iniciar um contêiner PostgreSQL na porta `5432`.
2. Criar um banco de dados chamado `rag`.
3. Ativar a extensão `vector` automaticamente.

### 3. Ingestão do PDF

Coloque o arquivo PDF que você deseja processar na raiz do projeto com o nome `document.pdf` (ou altere a variável `PDF_PATH` no `.env`).

Execute o script de ingestão:

```bash
python src/ingest.py
```

Este script irá ler o PDF, dividi-lo em pedaços, gerar os embeddings e armazená-los no banco de dados `pgvector`.

### 4. Iniciar o Chat

Após a ingestão, inicie o chat interativo:

```bash
python src/chat.py
```

O terminal ficará aguardando suas perguntas. Digite sua pergunta e pressione Enter. Para sair, digite `exit`.

## Configurações Adicionais

### Variáveis de Ambiente por Tecnologia

- **PostgreSQL (`docker-compose.yml`):**
  - `POSTGRES_USER`: `postgres`
  - `POSTGRES_PASSWORD`: `postgres`
  - `POSTGRES_DB`: `rag`

- **Aplicação (`.env`):**
  - `DATABASE_URL`: URL de conexão com o banco de dados.
  - `PG_VECTOR_COLLECTION_NAME`: Nome da coleção (tabela) no `pgvector`.
  - `PDF_PATH`: Caminho para o arquivo PDF a ser ingerido.
  - `LANGCHAIN_HANDLER`: Define qual LLM usar (`openai`, `google`, `azure`).

- **OpenAI:**
  - `OPENAI_API_KEY`: Sua chave de API.
  - `OPENAI_EMBEDDING_MODEL`: Modelo de embedding.
  - `OPENAI_LLM_MODEL`: Modelo de chat.

- **Google Gemini:**
  - `GOOGLE_API_KEY`: Sua chave de API.
  - `GOOGLE_EMBEDDING_MODEL`: Modelo de embedding.
  - `GOOGLE_LLM_MODEL`: Modelo de chat.

- **Azure OpenAI:**
  - `AZURE_OPENAI_API_KEY`: Sua chave de API.
  - `AZURE_OPENAI_ENDPOINT`: Endpoint do seu recurso Azure OpenAI.
  - `AZURE_OPENAI_API_VERSION`: Versão da API.
  - `AZURE_OPENAI_LLM_MODEL`: Nome do deployment do modelo de chat.
  - `AZURE_OPENAI_EMBEDDING_MODEL`: Nome do deployment do modelo de embedding.
  - `AZURE_OPENAI_EMBEDDING_ENDPOINT`: Endpoint do seu recurso de embedding (pode ser o mesmo do chat).
  - `AZURE_OPENAI_EMBEDDING_API_VERSION`: Versão da API de embedding.