from flask import Blueprint, request, jsonify
from app.api.auth import token_required
from datetime import datetime, timedelta
import random
import json

features_bp = Blueprint('features', __name__)

# Kerala-specific data
KERALA_DISTRICTS = [
    "Thiruvananthapuram", "Kollam", "Pathanamthitta", "Alappuzha", 
    "Kottayam", "Idukki", "Ernakulam", "Thrissur", "Palakkad", 
    "Malappuram", "Kozhikode", "Wayanad", "Kannur", "Kasaragod"
]

# Weather Data for Kerala
@features_bp.route('/weather/current')
def get_current_weather():
    location = request.args.get('location', 'Kochi')
    
    weather_data = {
        'location': f"{location}, Kerala",
        'temperature': random.randint(28, 35),
        'condition': random.choice(['Sunny', 'Partly Cloudy', 'Cloudy', 'Light Rain', 'Rainy']),
        'humidity': random.randint(65, 85),
        'windSpeed': random.randint(5, 15),
        'pressure': random.randint(1005, 1015),
        'visibility': random.randint(8, 12),
        'lastUpdated': datetime.utcnow().isoformat()
    }
    return jsonify(weather_data)

@features_bp.route('/weather/districts')
def get_district_weather():
    districts_weather = []
    for district in KERALA_DISTRICTS:
        districts_weather.append({
            'name': district,
            'temperature': random.randint(25, 35),
            'condition': random.choice(['Sunny', 'Partly Cloudy', 'Cloudy', 'Rainy']),
            'rainProbability': random.randint(10, 90)
        })
    return jsonify(districts_weather)

@features_bp.route('/weather/forecast')
def get_weekly_forecast():
    forecast = []
    for i in range(7):
        date = datetime.utcnow() + timedelta(days=i)
        forecast.append({
            'date': date.strftime('%Y-%m-%d'),
            'day': date.strftime('%A'),
            'high': random.randint(30, 35),
            'low': random.randint(24, 26),
            'condition': random.choice(['Sunny', 'Partly Cloudy', 'Cloudy', 'Rainy']),
            'rainProbability': random.randint(10, 80)
        })
    return jsonify(forecast)

@features_bp.route('/weather/advisory')
def get_crop_advisory():
    advisory = [
        {
            'crop': 'Rice',
            'advice': 'Ideal conditions for paddy transplantation. Maintain proper water level.',
            'status': 'good'
        },
        {
            'crop': 'Coconut',
            'advice': 'Moderate rainfall beneficial. Watch for waterlogging in low-lying areas.',
            'status': 'moderate'
        },
        {
            'crop': 'Spices',
            'advice': 'Harvest pepper and cardamom before expected heavy rains.',
            'status': 'urgent'
        },
        {
            'crop': 'Vegetables',
            'advice': 'Provide shade protection during sunny periods.',
            'status': 'warning'
        }
    ]
    return jsonify(advisory)

# Market Prices Data
@features_bp.route('/market/prices')
def get_market_prices():
    crop = request.args.get('crop', '')
    district = request.args.get('district', '')
    
    # Sample Kerala market prices
    prices = [
        {
            'commodity': 'Rice', 'variety': 'Ponni', 'market': 'Kochi Market', 
            'district': 'Ernakulam', 'price': 32.50, 'change': 2.3, 'unit': 'kg'
        },
        {
            'commodity': 'Rice', 'variety': 'Jaya', 'market': 'Trivandrum Market', 
            'district': 'Thiruvananthapuram', 'price': 30.75, 'change': -1.2, 'unit': 'kg'
        },
        {
            'commodity': 'Coconut', 'variety': 'Mature', 'market': 'Thrissur Market', 
            'district': 'Thrissur', 'price': 12.75, 'change': 0.5, 'unit': 'piece'
        },
        {
            'commodity': 'Vegetables', 'variety': 'Tomato', 'market': 'Kozhikode Market', 
            'district': 'Kozhikode', 'price': 28.30, 'change': 3.7, 'unit': 'kg'
        }
    ]
    
    # Filter based on query parameters
    if crop:
        prices = [p for p in prices if p['commodity'].lower() == crop.lower()]
    if district:
        prices = [p for p in prices if p['district'].lower() == district.lower()]
    
    return jsonify({
        'prices': prices,
        'lastUpdated': datetime.utcnow().isoformat()
    })

# Grievances API
@features_bp.route('/grievances', methods=['GET'])
@token_required
def get_grievances(current_user):
    # In real implementation, fetch from database
    grievances = [
        {
            'id': 1,
            'subject': 'Crop damage due to heavy rain',
            'category': 'Weather Damage',
            'status': 'pending',
            'date': '2024-01-15',
            'location': 'Alappuzha'
        }
    ]
    return jsonify({'grievances': grievances})

@features_bp.route('/grievances', methods=['POST'])
@token_required
def submit_grievance(current_user):
    data = request.get_json()
    
    grievance = {
        'id': random.randint(1000, 9999),
        'subject': data.get('subject'),
        'category': data.get('category'),
        'priority': data.get('priority'),
        'description': data.get('description'),
        'location': data.get('location'),
        'contact': data.get('contact'),
        'status': 'pending',
        'submittedBy': current_user.id,
        'submittedAt': datetime.utcnow().isoformat()
    }
    
    return jsonify({
        'success': True,
        'message': 'Grievance submitted successfully',
        'grievance': grievance
    })

# Subsidies API
@features_bp.route('/subsidies')
def get_subsidies():
    subsidies = [
        {
            'name': 'PM-KISAN Scheme',
            'description': 'Financial assistance of ₹6,000 per year to all farmer families',
            'amount': '₹6,000/year',
            'eligibility': 'All farmer families',
            'contact': '1800-115-526',
            'status': 'Active'
        },
        {
            'name': 'Kerala State Crop Insurance Scheme',
            'description': 'Insurance coverage for crops against natural calamities',
            'amount': 'Premium subsidy up to 50%',
            'eligibility': 'All registered farmers in Kerala',
            'contact': '0471-2327877',
            'status': 'Active'
        }
    ]
    return jsonify({'subsidies': subsidies})

# Government Schemes API
@features_bp.route('/govt-schemes')
def get_govt_schemes():
    schemes = [
        {
            'name': 'Kerala Agro-based Industries Scheme',
            'description': 'Support for setting up agro-based industries with subsidies',
            'benefits': '25-35% subsidy on project cost',
            'eligibility': 'Farmers and entrepreneurs',
            'contact': '0471-2326889'
        },
        {
            'name': 'Organic Farming Scheme Kerala',
            'description': 'Promotion of organic farming practices with financial support',
            'benefits': 'Subsidy for organic inputs and certification',
            'eligibility': 'Farmers practicing organic farming',
            'contact': '0471-2326990'
        }
    ]
    return jsonify({'schemes': schemes})