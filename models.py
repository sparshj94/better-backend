from datetime import datetime
import logging
from pymongo.errors import DuplicateKeyError, ConnectionFailure, ServerSelectionTimeoutError
from flask_pymongo import PyMongo
from nanoid import generate

logger = logging.getLogger(__name__)

# Initialize PyMongo with no arguments - will be initialized with app later
mongo = PyMongo()

def create_url(original_url):
    """Create a new shortened URL."""
    try:
        while True:
            # Generate a unique 6-character slug
            slug = generate(size=6)
            
            # Check if slug already exists
            if not mongo.db.urls.find_one({"slug": slug}):
                break
        
        url_doc = {
            "slug": slug,
            "originalUrl": original_url,
            "createdAt": datetime.utcnow(),
            "clickCount": 0,
            "lastClickedAt": None
        }
        
        mongo.db.urls.insert_one(url_doc)
        return url_doc
    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        logger.error(f"MongoDB connection error: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Error creating URL: {str(e)}")
        return None

def get_url_by_slug(slug):
    """Get URL document by slug."""
    try:
        return mongo.db.urls.find_one({"slug": slug})
    except Exception as e:
        logger.error(f"Error retrieving URL by slug: {str(e)}")
        return None

def increment_click_count(slug):
    """Increment click count for a URL and update lastClickedAt."""
    try:
        return mongo.db.urls.update_one(
            {"slug": slug},
            {
                "$inc": {"clickCount": 1},
                "$set": {"lastClickedAt": datetime.utcnow()}
            }
        )
    except Exception as e:
        logger.error(f"Error incrementing click count: {str(e)}")
        return None

def get_all_urls():
    """Get all URL documents."""
    try:
        return list(mongo.db.urls.find())
    except Exception as e:
        logger.error(f"Error retrieving all URLs: {str(e)}")
        return []

def get_analytics(slug):
    """Get analytics for a specific URL."""
    try:
        url_doc = mongo.db.urls.find_one(
            {"slug": slug},
            {"_id": 0, "clickCount": 1, "createdAt": 1, "lastClickedAt": 1}
        )
        return url_doc
    except Exception as e:
        logger.error(f"Error retrieving analytics: {str(e)}")
        return None