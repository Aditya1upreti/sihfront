from flask import Blueprint, request, jsonify, session
from app.models.user import User
from app import db
from datetime import datetime
import jwt
import os
from functools import wraps

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# JWT Secret Key (use environment variable in production)
JWT_SECRET = os.environ.get('JWT_SECRET', 'your-secret-key-here')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            if token.startswith('Bearer '):
                token = token[7:]
            data = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            current_user = User.query.get(data['user_id'])
            
            if not current_user:
                return jsonify({'error': 'Invalid token'}), 401
                
        except Exception as e:
            return jsonify({'error': 'Token is invalid'}), 401
            
        return f(current_user, *args, **kwargs)
        
    return decorated

def generate_token(user):
    payload = {
        'user_id': user.id,
        'uuid': user.uuid,
        'exp': datetime.utcnow().timestamp() + 24 * 3600  # 24 hours
    }
    return jwt.encode(payload, JWT_SECRET, algorithm='HS256')

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['email', 'password', 'first_name', 'last_name', 'phone']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Check if user already exists
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'User already exists with this email'}), 400
        
        # Create new user
        user = User(
            email=data['email'],
            phone=data['phone'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            state=data.get('state'),
            district=data.get('district'),
            village=data.get('village'),
            language=data.get('language', 'en')
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        # Generate token
        token = generate_token(user)
        
        return jsonify({
            'success': True,
            'message': 'User registered successfully',
            'token': token,
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Registration failed'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password are required'}), 400
        
        user = User.query.filter_by(email=data['email']).first()
        
        if not user or not user.check_password(data['password']):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Update last login
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        # Generate token
        token = generate_token(user)
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'token': token,
            'user': user.to_dict()
        })
        
    except Exception as e:
        return jsonify({'error': 'Login failed'}), 500

@auth_bp.route('/me', methods=['GET'])
@token_required
def get_current_user(current_user):
    return jsonify({
        'success': True,
        'user': current_user.to_dict()
    })

@auth_bp.route('/logout', methods=['POST'])
@token_required
def logout(current_user):
    # In a stateless JWT system, logout is handled client-side by removing the token
    return jsonify({'success': True, 'message': 'Logout successful'})

@auth_bp.route('/check-auth', methods=['GET'])
@token_required
def check_auth(current_user):
    return jsonify({
        'success': True,
        'authenticated': True,
        'user': current_user.to_dict()
    })