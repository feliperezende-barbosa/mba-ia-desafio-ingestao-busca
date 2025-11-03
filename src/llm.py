from .settings import LangChainHandlerEnum, Settings

from langchain_openai import ChatOpenAI, AzureChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

settings = Settings()

def get_llm_handler() -> ChatOpenAI | AzureChatOpenAI | ChatGoogleGenerativeAI:
  match settings.langchain.handler:
    case LangChainHandlerEnum.AZURE:
      return AzureChatOpenAI(
        azure_deployment=settings.azure.chat.model,
        model=settings.azure.chat.model,
        api_key=settings.azure.api_key,
        azure_endpoint=settings.azure.chat.endpoint,
        api_version=settings.azure.chat.api_version,
        temperature=0.4,
      )
    case LangChainHandlerEnum.OPENAI:
      return ChatOpenAI(
        model=settings.openai.llm_model,
        openai_api_key=settings.openai.openai_api_key,
        temperature=0,
      )
    case LangChainHandlerEnum.GOOGLE:
      return ChatGoogleGenerativeAI(
        model=settings.google_genai.llm_model,
        google_api_key=settings.google_genai.api_key,
        temperature=0,
      )
    case _:
      raise ValueError("Unsupported AI model: The values for LANGCHAIN_HANDLER are: 'openai', 'azure' or 'google'.")