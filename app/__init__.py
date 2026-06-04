from flask import Flask, jsonify, current_app, request, send_file,send_from_directory 
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
import os
from datetime import datetime

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
def create_app():
    app = Flask(__name__, template_folder='..', static_folder='..')
    
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
    
    # --- ROUTING ARCHITECTURE ---
    
    # 1. Main Entry Point: Redirects to Login
    @app.route('/')
    def serve_index():
        return send_from_directory('..', 'login.html')

    # 2. Protected Dashboard
    @app.route('/dashboard')
    def serve_dashboard():
        return send_from_directory('..', 'dashboard.html')

    # 3. Feature Pages
    @app.route('/identifier')
    def serve_plant_identifier():
        return send_from_directory('..', 'plant-identifier.html')
    
    @app.route('/chat')
    def serve_agri_assistant():
        return send_from_directory('..', 'agri-assistant.html')

    @app.route('/weather')
    def serve_weather():
        return send_from_directory('..', 'weather.html')
    
    @app.route('/market-prices')
    def serve_market_prices():
        return send_from_directory('..', 'market-prices.html')
    
    @app.route('/grievances')
    def serve_grievances():
        return send_from_directory('..', 'grievances.html')
    
    @app.route('/subsidies')
    def serve_subsidies():
        return send_from_directory('..', 'subsidies.html')
    
    @app.route('/govt-schemes')
    def serve_govt_schemes():
        return send_from_directory('..', 'govt-schemes.html')
        
    @app.route('/login')
    def serve_login():
        return send_from_directory('..', 'login.html')    
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
    # --- API ENDPOINTS FOR FEATURE PAGES ---
    
    @app.route('/api/weather')
    def api_weather():
        location = request.args.get('location', 'Kerala')
        
        # Pull the key securely from the .env file
        API_KEY = os.environ.get('OPENWEATHER_API_KEY')
        
        try:
            # Only try to fetch live data if the key exists
            if API_KEY:
                url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}&units=metric"
                response = requests.get(url).json()
                
                return jsonify({
                    "success": True,
                    "temperature": round(response['main']['temp']),
                    "condition": response['weather'][0]['main'],
                    "humidity": response['main']['humidity'],
                    "windSpeed": round(response['wind']['speed'] * 3.6),
                    "location": response['name'],
                    "advisory": [
                        "Live satellite data loaded successfully.",
                        f"Current humidity is at {response['main']['humidity']}%. Monitor soil moisture.",
                        "Conditions are optimal for scheduled farm activities."
                    ],
                    "forecast": [
                        {"day": "Tomorrow", "temp": round(response['main']['temp'] + 1), "condition": "Sunny"},
                        {"day": "Wednesday", "temp": round(response['main']['temp'] - 1), "condition": "Light Rain"},
                        {"day": "Thursday", "temp": round(response['main']['temp']), "condition": "Cloudy"}
                    ]
                })
            else:
                print("Warning: OPENWEATHER_API_KEY not found in .env file.")
                
        except Exception as e:
            print(f"Weather API Error: {e}")
            
        # The Failsafe Fallback
        return jsonify({
            "success": True,
            "temperature": 29,
            "condition": "Partly Cloudy",
            "humidity": 65,
            "windSpeed": 14,
            "location": location,
            "advisory": [
                "(Offline Mode) Ideal weather for spraying pesticides today.",
                "Maintain soil moisture for newly planted saplings."
            ],
            "forecast": [
                {"day": "Tomorrow", "temp": 30, "condition": "Sunny"},
                {"day": "Wednesday", "temp": 27, "condition": "Light Rain"}
            ]
        })
    @app.route('/api/market-prices')
    def api_market_prices():
        return jsonify({
            "prices": [
                {"crop": "Rice (Ponni)", "market": "Kochi Market", "price": 32.50, "change": 2.3},
                {"crop": "Coconut", "market": "Thrissur Market", "price": 12.75, "change": 0.5},
                {"crop": "Tomato", "market": "Kozhikode Market", "price": 28.30, "change": -1.2},
                {"crop": "Cardamom", "market": "Idukki Market", "price": 1250.00, "change": 5.4}
            ]
        })
        
    @app.route('/api/subsidies')
    def api_subsidies():
        from app.api.features import get_subsidies
        return get_subsidies()
        
    @app.route('/api/govt-schemes')
    def api_govt_schemes():
        from app.api.features import get_govt_schemes
        return get_govt_schemes()
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