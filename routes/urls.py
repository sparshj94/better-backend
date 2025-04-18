from flask import Blueprint, request, jsonify, redirect, current_app
import re

# Try relative import first, fall back to absolute import
try:
    from ..models import create_url, get_url_by_slug, increment_click_count, get_all_urls
except (ImportError, ValueError):
    from models import create_url, get_url_by_slug, increment_click_count, get_all_urls

url_bp = Blueprint('urls', __name__)

URL_REGEX = re.compile(
    r'^(?:http|https)://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain
    r'localhost|'  # localhost
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)

@url_bp.route('/api/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    
    if not data or 'url' not in data:
        return jsonify({"error": "URL is required"}), 400
    
    original_url = data['url']
    
    if not URL_REGEX.match(original_url):
        return jsonify({"error": "Invalid URL format"}), 400
    
    url_doc = create_url(original_url)
    base_url = current_app.config['BASE_URL']
    
    return jsonify({
        "slug": url_doc["slug"],
        "shortUrl": f"{base_url}/{url_doc['slug']}"
    }), 201

@url_bp.route('/<slug>', methods=['GET'])
def redirect_to_original(slug):
    url_doc = get_url_by_slug(slug)
    
    if not url_doc:
        return jsonify({"error": "URL not found"}), 404
    
    increment_click_count(slug)
    
    return redirect(url_doc["originalUrl"], code=302)

@url_bp.route('/api/urls', methods=['GET'])
def get_urls():
    urls = get_all_urls()
    
    # Convert ObjectID to string for JSON serialization
    for url in urls:
        url["_id"] = str(url["_id"])
        
        # Convert datetime objects to ISO format strings
        if "createdAt" in url:
            url["createdAt"] = url["createdAt"].isoformat()
        if "lastClickedAt" in url and url["lastClickedAt"]:
            url["lastClickedAt"] = url["lastClickedAt"].isoformat()
    
    return jsonify(urls), 200 