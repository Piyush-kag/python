import sys

from loguru import logger

# Configuration dictionary
config = {
    "handlers": [
        {"sink": sys.stdout, "level": "DEBUG"},
        {"sink": "app.log", "format": "{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}", "rotation": "10 MB",
         "retention": "10 days"},
        {"sink": "error.log", "level": "ERROR", "retention": "10 days"},
        {"sink": "exception.log", "level": "ERROR", "retention": "10 days"},
    ]
}
logger.configure(**config)
