from pydantic_settings import BaseSettings , SettingsConfigDict


class Settings(BaseSettings):
    
    APP_NAME : str
    APP_VERSION : str
    OPENROUTER_API_KEY: str
    
    FILE_ALLOWED_TYPES : list[str]
    FILE_MAX_SIZE : int
    FILE_DEFAULT_CHUNK_SIZE : int
    
    MONGODB_URL : str
    MONGODB_DATABASE:str
    
    class Config: ## Config is mandatory , only Pydantic understands it 
        env_file = ".env" ## same here
        


### a function that returns the .env variables
def get_settings():
    return Settings()