from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import find_dotenv

class Settings(BaseSettings):
    GEMINI_API_KEY:str
    GEMINI_MODEL:str
    model_config = SettingsConfigDict(env_file=find_dotenv(), extra='ignore')

def get_settings():
    return Settings()

settings = get_settings()