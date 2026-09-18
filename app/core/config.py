from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    NOCODB_BASE_URL: str
    NOCODB_API_TOKEN: str
    NOCODB_PROJECT_ID: str
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
