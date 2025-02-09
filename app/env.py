import os

from dotenv import find_dotenv, load_dotenv
from loguru import logger

####################################
# Load .env file
####################################

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(find_dotenv())

####################################
# Load environment variables
####################################

# Database
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')

DATABASE_NAME = os.getenv('DATABASE_NAME', 'ocr')
PDF_COLLECTION = os.getenv('PDF_COLLECTION', 'pdf')
RESULT_COLLECTION = os.getenv('RESULT_COLLECTION', 'result')

# OpenAI
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
OPENAI_BASE_URL = os.getenv('OPENAI_BASE_URL', 'https://api.openai.com/v1')

# FastAPI
FASTAPI_HOST = os.getenv('FASTAPI_HOST', '0.0.0.0')
FASTAPI_PORT = os.getenv('FASTAPI_PORT', '8000')

# Streamlit
STREAMLIT_PORT = os.getenv('STREAMLIT_PORT', '8501')

# Loguru
LOGURU_LEVEL = os.getenv('LOGURU_LEVEL', 'INFO')

# Models
MODELS = os.getenv('MODELS', 'gpt-4o-2024-11-20')

log_level = ['TRACE', 'DEBUG', 'INFO', 'SUCCESS', 'WARNING', 'ERROR', 'CRITICAL']
if LOGURU_LEVEL in log_level:
    # Modify log level
    logger.level(LOGURU_LEVEL)
else:
    # Default log level
    logger.level('INFO')

logger.info(f'Base directory: {BASE_DIR}')
