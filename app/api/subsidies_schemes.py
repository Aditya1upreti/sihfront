from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import random

subsidies_schemes_bp = Blueprint('subsidies_schemes', __name__)

# Kerala-specific subsidies data
KERALA_SUBSIDIES = [
    {
        'id': 1,
        'name': 'PM-KISAN Scheme',
        'name_ml': 'പിഎം-കിസാൻ പദ്ധതി',
        'category': 'crop',
        'amount': '₹6,000 per year',
        'percentage': '100%',
        'status': 'active',
        'eligibility': 'All farmer families owning cultivable land',
        'benefits': 'Financial assistance for cultivation expenses',
        'contact': '1800-115-526',
        'lastDate': '2024-12-31',
        'description': 'Central government scheme providing income support to all landholding farmer families'
    },
    {
        'id': 2,
        'name': 'Kerala Farm Mechanization Subsidy',
        'name_ml': 'കേരള ഫാം മെക്കാനൈസേഷൻ സബ്സിഡി',
        'category': 'equipment',
        'amount': 'Up to ₹5 lakhs',
        'percentage': '40-75%',
        'status': 'active',
        'eligibility': 'Farmers with minimum 0.5 acres land',
        'benefits': 'Subsidy for purchasing farm equipment and machinery',
        'contact': '0471-2326889',
        'lastDate': '2024-06-30',
        'description': 'Subsidy for purchasing agricultural machinery like tractors, harvesters, etc.'
    }
]

# Kerala-specific government schemes data
KERALA_SCHEMES = [
    {
        'id': 1,
        'name': 'Pradhan Mantri Fasal Bima Yojana',
        'name_ml': 'പ്രധാനമന്ത്രി ഫസൽ ബിമാ യോജന',
        'type': 'national',
        'benefits': 'Crop insurance against natural calamities',
        'eligibility': 'All farmers including sharecroppers and tenant farmers',
        'contact': '1800-110-001',
        'agency': 'Agriculture Insurance Company',
        'lastDate': '2024-12-31',
        'description': 'Comprehensive crop insurance scheme for farmers risk protection'
    },
    {
        'id': 2,
        'name': 'Kerala State Organic Farming Policy',
        'name_ml': 'കേരള സംസ്ഥാന ഓർഗാനിക് ഫാമിംഗ് പോളിസി',
        'type': 'state',
        'benefits': 'Support for organic farming and market linkage',
        'eligibility': 'Farmers practicing organic farming methods',
        'contact': '0471-2326777',
        'agency': 'Kerala Agriculture Department',
        'lastDate': '2024-08-15',
        'description': 'Promotion of organic farming practices in Kerala'
    }
]

@subsidies_schemes_bp.route('/subsidies')
def get_subsidies():
    category = request.args.get('category', '')
    status = request.args.get('status', '')
    district = request.args.get('district', '')
    
    filtered_subsidies = KERALA_SUBSIDIES
    
    if category:
        filtered_subsidies = [s for s in filtered_subsidies if s['category'] == category]
    
    if status:
        filtered_subsidies = [s for s in filtered_subsidies if s['status'] == status]
    
    return jsonify({
        'subsidies': filtered_subsidies,
        'total': len(filtered_subsidies),
        'lastUpdated': datetime.utcnow().isoformat()
    })

@subsidies_schemes_bp.route('/schemes')
def get_schemes():
    scheme_type = request.args.get('type', 'all')
    
    if scheme_type == 'all':
        filtered_schemes = KERALA_SCHEMES
    else:
        filtered_schemes = [s for s in KERALA_SCHEMES if s['type'] == scheme_type]
    
    return jsonify({
        'schemes': filtered_schemes,
        'total': len(filtered_schemes),
        'lastUpdated': datetime.utcnow().isoformat()
    })

@subsidies_schemes_bp.route('/subsidy/<int:subsidy_id>')
def get_subsidy_detail(subsidy_id):
    subsidy = next((s for s in KERALA_SUBSIDIES if s['id'] == subsidy_id), None)
    if subsidy:
        return jsonify({'subsidy': subsidy})
    return jsonify({'error': 'Subsidy not found'}), 404

@subsidies_schemes_bp.route('/scheme/<int:scheme_id>')
def get_scheme_detail(scheme_id):
    scheme = next((s for s in KERALA_SCHEMES if s['id'] == scheme_id), None)
    if scheme:
        return jsonify({'scheme': scheme})
    return jsonify({'error': 'Scheme not found'}), 404