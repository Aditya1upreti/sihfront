# app/api/__init__.py

from flask import Blueprint
from .auth import auth_bp
from .chat import chat_bp
from .ai import ai_bp
from .features import features_bp
from .subsidies_schemes import subsidies_schemes_bp

# Create a main API blueprint that groups all API routes
api_bp = Blueprint('api', __name__, url_prefix='/api')

# Register all sub-blueprints with the main API blueprint
def register_blueprints():
    """
    Register all API blueprints
    """
    api_bp.register_blueprint(auth_bp)
    api_bp.register_blueprint(chat_bp)
    api_bp.register_blueprint(ai_bp)
    api_bp.register_blueprint(features_bp)
    api_bp.register_blueprint(subsidies_schemes_bp)

# API version information
API_VERSION = '1.0.0'
API_TITLE = 'Krish-Sahayak Agricultural Assistant API'
API_DESCRIPTION = 'REST API for Krish-Sahayak agricultural assistance platform'

# API metadata
api_metadata = {
    'version': API_VERSION,
    'title': API_TITLE,
    'description': API_DESCRIPTION,
    'endpoints': {
        'authentication': {
            'login': 'POST /api/auth/login',
            'register': 'POST /api/auth/register',
            'logout': 'POST /api/auth/logout',
            'user_profile': 'GET /api/auth/me'
        },
        'chat': {
            'list_conversations': 'GET /api/chat/conversations',
            'create_conversation': 'POST /api/chat/conversations',
            'send_message': 'POST /api/chat/conversations/<id>/messages',
            'delete_conversation': 'DELETE /api/chat/conversations/<id>'
        },
        'ai_services': {
            'plant_analysis': 'POST /api/ai/analyze-plant',
            'recommendations': 'GET /api/ai/recommendations'
        },
        'features': {
            'weather': 'GET /api/weather/current',
            'market_prices': 'GET /api/market/prices',
            'grievances': 'GET/POST /api/grievances',
            'subsidies': 'GET /api/subsidies',
            'schemes': 'GET /api/schemes'
        }
    }
}

def get_api_info():
    """
    Return API information and available endpoints
    """
    return api_metadata

# Error handlers for API routes
def register_error_handlers(api_bp):
    """
    Register common error handlers for API routes
    """
    @api_bp.errorhandler(400)
    def bad_request(error):
        return {
            'error': 'Bad Request',
            'message': 'The request could not be understood or was missing required parameters.',
            'status_code': 400
        }, 400

    @api_bp.errorhandler(401)
    def unauthorized(error):
        return {
            'error': 'Unauthorized',
            'message': 'Authentication failed or user does not have permissions for the requested operation.',
            'status_code': 401
        }, 401

    @api_bp.errorhandler(404)
    def not_found(error):
        return {
            'error': 'Not Found',
            'message': 'The requested resource was not found.',
            'status_code': 404
        }, 404

    @api_bp.errorhandler(500)
    def internal_server_error(error):
        return {
            'error': 'Internal Server Error',
            'message': 'An internal server error occurred.',
            'status_code': 500
        }, 500

# API rate limiting decorator (placeholder for future implementation)
def rate_limit(requests_per_minute=60):
    """
    Decorator for rate limiting API endpoints
    """
    def decorator(f):
        def decorated_function(*args, **kwargs):
            # Rate limiting logic would go here
            # For now, just pass through
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# API response formatting
def format_response(data=None, message="Success", status_code=200, pagination=None):
    """
    Standard API response format
    """
    response = {
        'success': status_code < 400,
        'message': message,
        'data': data,
        'timestamp': None  # Will be set in the actual implementation
    }
    
    if pagination:
        response['pagination'] = pagination
        
    return response, status_code

# Initialize the API package
def init_api(app):
    """
    Initialize the API package with the Flask app
    """
    register_blueprints()
    register_error_handlers(api_bp)
    app.register_blueprint(api_bp)
    print("✅ API package initialized successfully")

# Export the main API blueprint and initialization function
__all__ = ['api_bp', 'init_api', 'get_api_info', 'format_response', 'rate_limit']

print("✅ API package imported successfully")