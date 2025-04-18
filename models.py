from datetime import datetime
from pymongo.errors import DuplicateKeyError
from flask_pymongo import PyMongo
from nanoid import generate

mongo = PyMongo()

def create_url(original_url):
    """Create a new shortened URL."""
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

def get_url_by_slug(slug):
    """Get URL document by slug."""
    return mongo.db.urls.find_one({"slug": slug})

def increment_click_count(slug):
    """Increment click count for a URL and update lastClickedAt."""
    return mongo.db.urls.update_one(
        {"slug": slug},
        {
            "$inc": {"clickCount": 1},
            "$set": {"lastClickedAt": datetime.utcnow()}
        }
    )

def get_all_urls():
    """Get all URL documents."""
    return list(mongo.db.urls.find())

def get_analytics(slug):
    """Get analytics for a specific URL."""
    url_doc = mongo.db.urls.find_one(
        {"slug": slug},
        {"_id": 0, "clickCount": 1, "createdAt": 1, "lastClickedAt": 1}
    )
    return url_doc 