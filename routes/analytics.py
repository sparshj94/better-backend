from flask import Blueprint, jsonify

# Try relative import first, fall back to absolute import
try:
    from ..models import get_analytics, get_url_by_slug
except (ImportError, ValueError):
    from models import get_analytics, get_url_by_slug

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/api/analytics/<slug>', methods=['GET'])
def get_url_analytics(slug):
    # Check if URL exists
    url_doc = get_url_by_slug(slug)
    if not url_doc:
        return jsonify({"error": "URL not found"}), 404
    
    # Get analytics data
    analytics_data = get_analytics(slug)
    
    # Convert datetime objects to ISO format
    if analytics_data["createdAt"]:
        analytics_data["createdAt"] = analytics_data["createdAt"].isoformat()
    if analytics_data["lastClickedAt"]:
        analytics_data["lastClickedAt"] = analytics_data["lastClickedAt"].isoformat()
    
    return jsonify(analytics_data), 200 