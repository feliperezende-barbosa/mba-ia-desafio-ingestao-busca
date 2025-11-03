from enum import Enum
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os

load_dotenv()

class LangChainHandlerEnum(str, Enum):
  OPENAI = "openai"
  AZURE = "azure"
  GOOGLE = "google"

class OpenAI(BaseModel):
  openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
  embedding_model: str = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
  llm_model: str = os.getenv("OPENAI_LLM_MODEL", "gpt-5-nano")

class AzureOpenAIChat(BaseModel):
  endpoint: str = os.getenv("AZURE_OPENAI_ENDPOINT", "")
  model: str = os.getenv("AZURE_OPENAI_LLM_MODEL", "gpt-5-nano")
  api_version: str = os.getenv("AZURE_OPENAI_API_VERSION", "")

class AzureOpenAIEmbeddings(BaseModel):
  endpoint: str = os.getenv("AZURE_OPENAI_EMBEDDING_ENDPOINT", "")
  api_version: str = os.getenv("AZURE_OPENAI_EMBEDDING_API_VERSION", "")
  model: str = os.getenv("AZURE_OPENAI_EMBEDDING_MODEL", "text-embedding-3-large")

class AzureOpenAIChat(BaseModel):
  chat: AzureOpenAIChat = Field(default_factory=AzureOpenAIChat)
  embeddings: AzureOpenAIEmbeddings = Field(default_factory=AzureOpenAIEmbeddings)
  api_key: str = os.getenv("AZURE_OPENAI_API_KEY", "")

class GoogleGenAI(BaseModel):
  api_key: str = os.getenv("GOOGLE_API_KEY", "")
  embedding_model: str = os.getenv("GOOGLE_EMBEDDING_MODEL", "models/embedding-001")
  llm_model: str = os.getenv("GOOGLE_LLM_MODEL", "gemini-2.5-flash-lite")

class DatabaseConfig(BaseModel):
  url: str = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost:5432/rag")
  collection_name: str = os.getenv("PG_VECTOR_COLLECTION_NAME", "")
  pdf_path: str = os.getenv("PDF_PATH", "document.pdf")

class LangChainConfig(BaseModel):
  handler: LangChainHandlerEnum = os.getenv("LANGCHAIN_HANDLER", LangChainHandlerEnum.OPENAI)

class Settings(BaseModel):
  openai: OpenAI = Field(default_factory=OpenAI)
  azure: AzureOpenAIChat = Field(default_factory=AzureOpenAIChat)
  google_genai: GoogleGenAI = Field(default_factory=GoogleGenAI)
  database: DatabaseConfig = Field(default_factory=DatabaseConfig)
  langchain: LangChainConfig = Field(default_factory=LangChainConfig)
