from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Application configuration managed by Pydantic.
    Values are automatically populated from environment variables or the local .env file.
    """
    # --- Server Settings ---
    PROJECT_NAME: str = "AI Insurance Policy Auditor"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"
    PORT: int = 8000

    # --- LLM Provider Config ---
    # Without a default value, Pydantic will throw an error on startup if this is missing
    OPENAI_API_KEY: str

    # --- Tooling API Keys ---
    TAVILY_API_KEY: str

    # --- LangChain / LangSmith Tracing (Observability) ---
    # These are highly recommended for debugging LangGraph's cyclical ReAct loops
    LANGCHAIN_TRACING_V2: str = "false"
    LANGCHAIN_API_KEY: Optional[str] = None
    LANGCHAIN_PROJECT: str = "Insurance_Auditor_Agent"

    # Instruct Pydantic to read from the .env file located at the root directory.
    # extra="ignore" allows other variables to exist in .env without throwing validation errors.
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

# Instantiate the settings object to be imported across the application
settings = Settings()