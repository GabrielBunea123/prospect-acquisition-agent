from functools import lru_cache
from typing import Annotated, Union, Literal

from dotenv import load_dotenv
from pydantic import Field, BaseModel
from pydantic.types import Tag
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.prospect_acquisition_agent.models.llm import ProviderType as LLMProviderType
from src.prospect_acquisition_agent.models.vector_store import (
    ProviderType as VectorStoreProviderType,
)

load_dotenv()


class ApiSettings(BaseModel):
    """Api Settings that can be overridden by env variables"""

    host: str = Field(default="0.0.0.0")
    port: int = Field(default=5000)


class LLMOpenAISettings(BaseModel):
    """Configuration for LLM Provider"""

    provider: Literal[LLMProviderType.OPENAI] = LLMProviderType.OPENAI
    api_key: str = Field(description="API Key")
    api_version: str = Field(description="API Version")
    model: str = Field(description="Model Name")
    base_url: str | None = Field(default=None, description="Base URL")
    temperature: float = Field(
        default=0.7, description="Temperature for response generation"
    )


LLMSettings = Annotated[
    Union[Annotated[LLMOpenAISettings, Tag("OPENAI")],],
    Field(discriminator="provider"),
]


class EmbeddingsOpenAISettings(BaseModel):
    """
    Configuration for OpenAI Embeddings
    """

    provider: Literal[LLMProviderType.OPENAI] = LLMProviderType.OPENAI
    api_key: str = Field(description="OpenAI API key")
    api_version: str = Field(description="OpenAI API version")
    model: str = Field(description="Model name to use")
    base_url: str | None = Field(default=None, description="Custom base URL")


EmbeddingsSettings = Annotated[
    Union[Annotated[EmbeddingsOpenAISettings, Tag("OPENAI")],],
    Field(discriminator="provider"),
]

LogLevel = Literal["NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class PGVectorStoreSettings(BaseModel):
    """
    Configuration for PostgresSQL Vector Store
    """

    provider: Literal[VectorStoreProviderType.PG_VECTOR] = (
        VectorStoreProviderType.PG_VECTOR
    )
    connection_string: str = Field(description="PostgresSQL connection string")
    schema_name: str = Field(description="Name of the database schema.")
    table_name: str = Field(description="Name of an existing table")
    id_column: str = Field(description="Column that represents the Document's id")
    metadata_json_column: str = Field("Column to store metadata as JSON.")


VectorStoreSettings = Annotated[
    Union[Annotated[PGVectorStoreSettings, Tag("PG_VECTOR")],],
    Field(discriminator="provider"),
]


class LoggingSettings(BaseModel):
    level: Annotated[LogLevel, Field(default="INFO")]
    trace_id_header: str = Field(
        default="X-Request-Id", description="HTTP header name for trace ID"
    )


class LLMTracingSettings(BaseModel):
    enabled: bool = Field(default=False, description="Enable LLM Tracing")


class ApolloAPISettings(BaseModel):
    api_key: str = Field(description="Apollo API Key")


class AppSettings(BaseSettings):
    """
    App Settings that can be overridden by env variables
    Nested properties should use "__" as delimiter (e.g: API__HOST, API__PORT)
    """

    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_nested_delimiter="__",
    )

    api: ApiSettings = Field(default_factory=ApiSettings)
    llm: Annotated[
        LLMSettings,
        Field(discriminator="provider", description="LLM Provider Configuration"),
    ]

    embeddings: Annotated[
        EmbeddingsSettings,
        Field(discriminator="provider", description="Embedder Provider Configuration"),
    ]

    vector_store: Annotated[
        PGVectorStoreSettings,
        Field(
            discriminator="provider",
            description="Vector store provider configuration",
        ),
    ]
    logging: LoggingSettings = Field(default_factory=LoggingSettings)

    llm_tracing: LLMTracingSettings = Field(default_factory=LLMTracingSettings)

    apollo_api: ApolloAPISettings = Field(default_factory=ApolloAPISettings)


@lru_cache()
def get_app_settings():
    return AppSettings()
