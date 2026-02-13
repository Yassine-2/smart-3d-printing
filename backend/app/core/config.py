import os
from pathlib import Path
from typing import Optional

class Settings:
    APP_NAME: str = "Smart 3D Printing"
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # AI Model Configuration
    MODEL_PATH: str = os.getenv("MODEL_PATH", "app/ai/models/my_model.pt")
    CONFIDENCE_THRESHOLD: float = float(os.getenv("CONFIDENCE_THRESHOLD", "0.6"))
    
    # Camera Configuration
    CAMERA_INDEX: int = int(os.getenv("CAMERA_INDEX", "0"))
    
    @classmethod
    def get_model_path(cls) -> Path:
        """Get model path as Path object, checking if it exists."""
        return Path(cls.MODEL_PATH)
    
    @classmethod
    def model_exists(cls) -> bool:
        """Check if model file exists."""
        return cls.get_model_path().exists()

settings = Settings()
