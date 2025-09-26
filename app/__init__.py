from flask import Flask, send_file, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
import os
from datetime import datetime

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config.from_object('app.config.DevelopmentConfig')
    
    # Initialize extensions
    CORS(app, origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:5000"], supports_credentials=True)
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Import and initialize models
    from app.models import init_models, setup_relationships
    init_models(app)
    setup_relationships()
    
    # Import and initialize API
    from app.api import init_api
    init_api(app)
    
    # Serve main pages
    @app.route('/')
    def serve_plant_identifier():
        try:
            return send_file('../plant-identifier.html')
        except Exception as e:
            return jsonify({'error': f'Error serving plant-identifier.html: {str(e)}'}), 500
    
    @app.route('/chat')
    def serve_agri_assistant():
        try:
            return send_file('../agri-assistant.html')
        except Exception as e:
            return jsonify({'error': f'Error serving agri-assistant.html: {str(e)}'}), 500
    
    @app.route('/login')
    def serve_login():
        try:
            return send_file('../login.html')
        except Exception as e:
            return jsonify({'error': f'Error serving login.html: {str(e)}'}), 500
    
    @app.route('/dashboard')
    def serve_dashboard():
        try:
            return send_file('../dashboard.html')
        except Exception as e:
            return jsonify({'error': f'Error serving dashboard.html: {str(e)}'}), 500
    
    # Serve feature pages
    @app.route('/weather')
    def serve_weather():
        try:
            return send_file('../weather.html')
        except Exception as e:
            return jsonify({'error': f'Error serving weather.html: {str(e)}'}), 500
    
    @app.route('/market-prices')
    def serve_market_prices():
        try:
            return send_file('../market-prices.html')
        except Exception as e:
            return jsonify({'error': f'Error serving market-prices.html: {str(e)}'}), 500
    
    @app.route('/grievances')
    def serve_grievances():
        try:
            return send_file('../grievances.html')
        except Exception as e:
            return jsonify({'error': f'Error serving grievances.html: {str(e)}'}), 500
    
    @app.route('/subsidies')
    def serve_subsidies():
        try:
            return send_file('../subsidies.html')
        except Exception as e:
            return jsonify({'error': f'Error serving subsidies.html: {str(e)}'}), 500
    
    @app.route('/govt-schemes')
    def serve_govt_schemes():
        try:
            return send_file('../govt-schemes.html')
        except Exception as e:
            return jsonify({'error': f'Error serving govt-schemes.html: {str(e)}'}), 500
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return jsonify({
            'status': 'healthy', 
            'service': 'Krish-Sahayak API',
            'timestamp': datetime.utcnow().isoformat(),
            'version': '1.0.0',
            'database': 'connected'  # You can add database connection check here
        })
    
    # API documentation endpoint
    @app.route('/api/docs')
    def api_documentation():
        from app.api import get_api_info
        return jsonify(get_api_info())
    
    # Root API endpoint
    @app.route('/api')
    def api_root():
        return jsonify({
            'message': 'Krish-Sahayak API Server',
            'version': '1.0.0',
            'endpoints': {
                'authentication': '/api/auth',
                'chat': '/api/chat',
                'ai_services': '/api/ai',
                'features': '/api/weather, /api/market-prices, etc.',
                'subsidies_schemes': '/api/subsidies, /api/schemes',
                'documentation': '/api/docs'
            }
        })
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        if request.path.startswith('/api/'):
            return jsonify({
                'error': 'Endpoint not found',
                'path': request.path,
                'status_code': 404
            }), 404
        return "Page not found", 404
    
    @app.errorhandler(500)
    def internal_error(error):
        if request.path.startswith('/api/'):
            return jsonify({
                'error': 'Internal server error',
                'status_code': 500
            }), 500
        return "Internal server error", 500
    
    # Logging setup (basic)
    @app.before_request
    def log_request_info():
        app.logger.debug(f'Request: {request.method} {request.path}')
    
    @app.after_request
    def log_response_info(response):
        app.logger.debug(f'Response: {response.status_code}')
        return response

    print("✅ Flask application initialized successfully")
    return app

# This allows running the app directly with python app/__init__.py
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)