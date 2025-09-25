from flask import Blueprint, request, jsonify
from app.api.auth import token_required
from datetime import datetime
import random

features_bp = Blueprint('features', __name__)

# Mock data for demonstration
WEATHER_DATA = {
    'temperature': random.randint(25, 35),
    'condition': 'Partly Cloudy',
    'humidity': random.randint(60, 85),
    'windSpeed': random.randint(5, 15),
    'advisory': [
        'Good day for rice cultivation activities',
        'Moderate rainfall expected tomorrow',
        'Ideal conditions for vegetable crops'
    ]
}

MARKET_PRICES = {
    'prices': [
        {'crop': 'Rice', 'market': 'Thrissur Market', 'price': 28.50, 'change': 2.3},
        {'crop': 'Coconut', 'market': 'Kozhikode Market', 'price': 12.75, 'change': -1.2},
        {'crop': 'Banana', 'market': 'Ernakulam Market', 'price': 18.00, 'change': 3.7},
        {'crop': 'Vegetables', 'market': 'Palakkad Market', 'price': 22.30, 'change': 0.8},
        {'crop': 'Spices', 'market': 'Kannur Market', 'price': 45.60, 'change': 4.1}
    ]
}

SUBSIDIES_DATA = {
    'subsidies': [
        {
            'name': 'PM-KISAN Scheme',
            'description': 'Financial assistance to farmers',
            'amount': '₹6,000/year',
            'eligibility': 'All farmer families',
            'status': 'Active'
        },
        {
            'name': 'Soil Health Card Scheme',
            'description': 'Soil testing and recommendations',
            'amount': 'Free testing',
            'eligibility': 'All farmers',
            'status': 'Active'
        }
    ]
}

GOVT_SCHEMES = {
    'schemes': [
        {
            'name': 'National Agriculture Market (e-NAM)',
            'description': 'Online trading platform for agricultural commodities',
            'benefits': 'Better price discovery, transparent trade',
            'contact': '1800-180-1551'
        },
        {
            'name': 'Pradhan Mantri Fasal Bima Yojana',
            'description': 'Crop insurance scheme',
            'benefits': 'Risk protection, financial support',
            'contact': '1800-110-001'
        }
    ]
}

@features_bp.route('/weather')
def get_weather():
    location = request.args.get('location', 'Kerala')
    # In real implementation, fetch from weather API
    return jsonify(WEATHER_DATA)

@features_bp.route('/market-prices')
def get_market_prices():
    crop = request.args.get('crop', '')
    # Filter by crop if specified
    if crop:
        filtered_prices = [p for p in MARKET_PRICES['prices'] if p['crop'].lower() == crop.lower()]
        return jsonify({'prices': filtered_prices})
    return jsonify(MARKET_PRICES)

@features_bp.route('/subsidies')
def get_subsidies():
    return jsonify(SUBSIDIES_DATA)

@features_bp.route('/govt-schemes')
def get_govt_schemes():
    return jsonify(GOVT_SCHEMES)

@features_bp.route('/grievances', methods=['GET'])
@token_required
def get_grievances(current_user):
    # In real implementation, fetch from database
    return jsonify({'grievances': []})

@features_bp.route('/grievances', methods=['POST'])
@token_required
def submit_grievance(current_user):
    data = request.get_json()
    # In real implementation, save to database
    return jsonify({
        'success': True,
        'message': 'Grievance submitted successfully',
        'grievance_id': f"GRV{datetime.now().strftime('%Y%m%d%H%M%S')}"
    })