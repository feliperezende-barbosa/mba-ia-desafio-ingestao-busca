from langchain_postgres import PGVector
from langchain_core.prompts import ChatPromptTemplate

from .embeddings import get_embeddings_handler
from .llm import get_llm_handler
from .settings import Settings

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""
settings = Settings()
embeddings = get_embeddings_handler()
llm = get_llm_handler()

def search_prompt(question: str) -> str:
  try:     
    vector_store = PGVector(
      embeddings=embeddings,
      collection_name=settings.database.collection_name,
      connection=settings.database.url,
    )

    retriever = vector_store.similarity_search(
      query=question,
      k=10,
    )
    
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

    chain = {
      "contexto": format_search_results(retriever),
      "pergunta": question
    }

    formatted_prompt = prompt.format(**chain)

    response = llm.invoke(formatted_prompt)
    return response.content
  
  except Exception as e:
    print(f"Erro ao buscar o prompt: {e}")
    return "Desculpe, ocorreu um erro ao processar sua solicitação."

def format_search_results(docs) -> str:
    return "\n".join(doc.page_content for doc in docs)
