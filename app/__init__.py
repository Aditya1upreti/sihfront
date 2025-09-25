from flask import Flask, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
# Add this to your existing __init__.py
from app.api.features import features_bp

# Register the blueprint
app.register_blueprint(features_bp)

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config.from_object('app.config.DevelopmentConfig')
    
    # Initialize extensions
    CORS(app, origins=["http://localhost:3000", "http://127.0.0.1:3000"], supports_credentials=True)
    db.init_app(app)
    
    # Register blueprints
    from app.api.chat import chat_bp
    from app.api.ai import ai_bp
    from app.api.auth import auth_bp
    
    app.register_blueprint(chat_bp)
    app.register_blueprint(ai_bp)
    app.register_blueprint(auth_bp)
    
    # Serve main pages
    @app.route('/')
    def serve_plant_identifier():
        return send_file('../plant-identifier.html')
    
    @app.route('/chat')
    def serve_agri_assistant():
        return send_file('../agri-assistant.html')
    
    @app.route('/login')
    def serve_login():
        return send_file('../login.html')
    
    @app.route('/dashboard')
    def serve_dashboard():
        return send_file('../dashboard.html')
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return jsonify({'status': 'healthy', 'service': 'Krish-Sahayak API'})
    
    return app