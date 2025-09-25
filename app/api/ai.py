from flask import Blueprint, request, jsonify
from app.services.ai_services import analyze_plant_image, generate_recommendations
from app.models.chat import Conversation, Message
from app.models.user import User
from app import db
import base64
import re

ai_bp = Blueprint('ai', __name__, url_prefix='/api/ai')

@ai_bp.route('/analyze-plant', methods=['POST'])
def analyze_plant():
    try:
        data = request.get_json()
        image_data = data.get('image_data')
        mime_type = data.get('mime_type')
        language = data.get('language', 'en-US')
        
        if not all([image_data, mime_type]):
            return jsonify({'error': 'Image data and MIME type are required'}), 400
        
        # Clean the base64 data if it contains data URL prefix
        if 'base64,' in image_data:
            image_data = image_data.split('base64,')[1]
        
        # Analyze the plant image
        analysis_result = analyze_plant_image(image_data, mime_type, language)
        
        return jsonify({'analysis': analysis_result})
    
    except Exception as e:
        return jsonify({'error': 'Failed to analyze plant image'}), 500

@ai_bp.route('/recommendations', methods=['GET'])
def get_recommendations():
    try:
        user_id = request.args.get('userId')
        if not user_id:
            return jsonify({'error': 'User ID is required'}), 400
        
        user = User.query.filter_by(uuid=user_id).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Get user's conversations
        conversations = Conversation.query.filter_by(user_id=user.id).all()
        if not conversations:
            return jsonify({'error': 'No conversation history found'}), 404
        
        # Extract chat history
        chat_history = ""
        for conv in conversations:
            messages = Message.query.filter_by(conversation_id=conv.id).order_by(Message.timestamp).all()
            for msg in messages:
                chat_history += f"{msg.sender}: {msg.content}\n"
            chat_history += "\n---\n\n"
        
        # Generate recommendations
        recommendations = generate_recommendations(chat_history)
        
        return jsonify({'recommendations': recommendations})
    
    except Exception as e:
        return jsonify({'error': 'Failed to generate recommendations'}), 500