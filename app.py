from flask import Flask
from flask_cors import CORS
import logging
import sys

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Use conditional imports to handle both package and direct execution
try:
    # When imported as a module
    from .config import Config
    from .models import mongo
    from .routes.urls import url_bp
    from .routes.analytics import analytics_bp
except ImportError:
    # When run directly as a script
    from config import Config
    from models import mongo
    from routes.urls import url_bp
    from routes.analytics import analytics_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Log configuration details (without sensitive info)
    logger.info(f"Starting application with BASE_URL: {config_class.BASE_URL}")
    logger.info(f"MONGO_URI configured: {'Yes' if config_class.MONGO_URI else 'No'}")
    
    # Initialize extensions
    CORS(app, resources={r"/api/*": {"origins": config_class.CORS_ORIGINS}})
    mongo.init_app(app)
    
    # Create MongoDB index for slug (if it doesn't exist)
    with app.app_context():
        try:
            if not mongo.db:
                logger.error("MongoDB connection failed. Check your MONGO_URI environment variable.")
            else:
                mongo.db.urls.create_index("slug", unique=True)
                logger.info("MongoDB connected successfully and index created.")
        except Exception as e:
            logger.error(f"Error during MongoDB setup: {str(e)}")
    
    # Register blueprints
    app.register_blueprint(url_bp)
    app.register_blueprint(analytics_bp)
    
    @app.route('/')
    def health_check():
        return {"status": "ok", "message": "URL Shortener API is running"}
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)