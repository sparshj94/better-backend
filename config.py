import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev_key')
    MONGO_URI = os.getenv('MONGO_URI')
    BASE_URL = os.getenv('BASE_URL', 'http://localhost:5000')
    CORS_ORIGINS = [
        'http://localhost:3000',
        'http://127.0.0.1:3000',
        'http://localhost:5173',  # Vite's default port
        'http://127.0.0.1:5173'
    ] 