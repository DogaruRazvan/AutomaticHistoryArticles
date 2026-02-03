from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env", env_file_encoding='utf-8')

    WIKI_BASE_URL: str = "https://en.wikipedia.org/api/rest_v1"
    USER_AGENT: str = "HistoryApp/1.0 (contact@example.com)"
    AI_MODEL: str = "llama-3.3-70b-versatile"  # <--- SCHIMBĂ AICI
    GROQ_API_KEY: str
    CLOUDINARY_CLOUD_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str

# Aceasta este linia care lipsește și cauzează eroarea:
config = Settings()