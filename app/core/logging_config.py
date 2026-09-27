import logging
import os
import sys
from config.settings import get_settings

settings = get_settings()

def setup_logging():
    os.makedirs("logs", exist_ok=True)
    
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    
    level = logging.DEBUG if settings.DEBUG else logging.INFO
    
    logging.basicConfig(
        level=level,
        format=log_format,
        datefmt=date_format,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("logs/app.log")
        ]
    )
    
    # Create distinct loggers
    app_logger = logging.getLogger("app")
    ai_logger = logging.getLogger("ai")
    api_logger = logging.getLogger("api")
    security_logger = logging.getLogger("security")
    
    return app_logger, ai_logger, api_logger, security_logger
