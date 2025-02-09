from app.env import (BASE_DIR, DATABASE_NAME, FASTAPI_HOST, FASTAPI_PORT,
                     LOGURU_LEVEL, MODELS, MONGO_URI, OPENAI_API_KEY,
                     OPENAI_BASE_URL, PDF_COLLECTION, REDIS_URL,
                     RESULT_COLLECTION, STREAMLIT_PORT)


class Config:
    def __init__(self):
        self.BASE_DIR = BASE_DIR
        self.FASTAPI_HOST = FASTAPI_HOST
        self.FASTAPI_PORT = FASTAPI_PORT
        self.STREAMLIT_PORT = STREAMLIT_PORT
        self.LOGURU_LEVEL = LOGURU_LEVEL
        self.OPENAI_API_KEY = OPENAI_API_KEY
        self.OPENAI_BASE_URL = OPENAI_BASE_URL
        self.REDIS_URL = REDIS_URL
        self.MONGO_URI = MONGO_URI
        self.MODELS = MODELS
        self.DATABASE_NAME = DATABASE_NAME
        self.PDF_COLLECTION = PDF_COLLECTION
        self.RESULT_COLLECTION = RESULT_COLLECTION


config = Config()
