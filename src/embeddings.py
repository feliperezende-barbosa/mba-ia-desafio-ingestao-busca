from .settings import LangChainHandlerEnum, Settings

from langchain_openai import OpenAIEmbeddings, AzureOpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings

settings = Settings()

def get_embeddings_handler() -> OpenAIEmbeddings | AzureOpenAIEmbeddings | GoogleGenerativeAIEmbeddings:
  match settings.langchain.handler:
    case LangChainHandlerEnum.AZURE:
      return AzureOpenAIEmbeddings(
        azure_deployment=settings.azure.embeddings.model,
        model=settings.azure.embeddings.model,
        api_key=settings.azure.api_key,
        azure_endpoint=settings.azure.embeddings.endpoint,
        api_version=settings.azure.embeddings.api_version,
      )
    case LangChainHandlerEnum.OPENAI:
      return OpenAIEmbeddings(
        model=settings.openai.embedding_model,
        openai_api_key=settings.openai.openai_api_key,
      )
    case LangChainHandlerEnum.GOOGLE:
      return GoogleGenerativeAIEmbeddings(
        model=settings.google_genai.embedding_model,
        google_api_key=settings.google_genai.api_key,
      )
    case _:
      raise ValueError("Unsupported AI model: The values for LANGCHAIN_HANDLER are: 'openai', 'azure' or 'google'.")