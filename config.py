import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev_key')
    
    # Use MONGODB_URI as fallback (Render uses this by default)
    MONGO_URI = os.getenv('MONGO_URI') or os.getenv('MONGODB_URI')
    
    # Handle multiple possible production URLs
    BASE_URL = os.getenv('BASE_URL', 'http://localhost:5000')
    
    # Add production frontend URLs for CORS
    CORS_ORIGINS = [
        'http://localhost:3000',
        'http://127.0.0.1:3000',
        'http://localhost:5173',  # Vite's default port
        'http://127.0.0.1:5173'
    ]
    
    # Add production domains from environment if they exist
    production_frontend = os.getenv('FRONTEND_URL')
    if production_frontend:
        CORS_ORIGINS.append(production_frontend)
        
    render_frontend = os.getenv('RENDER_EXTERNAL_URL')
    if render_frontend:
        CORS_ORIGINS.append(render_frontend)