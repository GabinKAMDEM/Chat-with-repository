"""Load global settings and project paths.

Settings are pulled from ``.env`` or environment variables so nothing
sensitive is committed.  ``DATA_DIR`` is created on import so that any
module can safely write files there.
"""

from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field      


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"

class Settings(BaseSettings):
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    repo_url: str = Field(..., env="REPO_URL")
    chroma_collection: str = Field("repo_index", env="CHROMA_COLLECTION")
    llm_model: str = Field("gpt-4o", env="LLM_MODEL")
    embedding_model: str = Field("text-embedding-3-small", env="EMBEDDING_MODEL")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()          # importable partout
DATA_DIR.mkdir(exist_ok=True)
