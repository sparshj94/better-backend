from flask import Flask
from flask_cors import CORS

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
    
    # Initialize extensions
    CORS(app, resources={r"/api/*": {"origins": config_class.CORS_ORIGINS}})
    mongo.init_app(app)
    
    # Create MongoDB index for slug (if it doesn't exist)
    with app.app_context():
        mongo.db.urls.create_index("slug", unique=True)
    
    # Register blueprints
    app.register_blueprint(url_bp)
    app.register_blueprint(analytics_bp)
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True) 