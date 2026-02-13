from pydantic import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Smart 3D Printing"
    DEBUG: bool = True

settings = Settings()
