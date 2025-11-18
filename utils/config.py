from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str
    APP_VESRION: str
    OPENAI_API_KEY: str
    OPENAI_MODEL_NAME:str
    OPENAI_API_BASE:str
    
    FILE_ALLOWED_TYPES: list
    FILE_MAX_SIZE: float

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"   
        
def get_settings(): 
    return Settings()