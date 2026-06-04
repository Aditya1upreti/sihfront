from flask import Blueprint, request, jsonify
from app.services.ai_services import analyze_plant_image, generate_recommendations
from app.models.chat import Conversation, Message
from app.models.user import User
from app import db
import base64
import re

ai_bp = Blueprint('ai', __name__, url_prefix='/ai')
@ai_bp.route('/analyze-plant', methods=['POST'])
@ai_bp.route('/analyze-plant', methods=['POST'])
def analyze_plant():
    try:
        data = request.get_json()
        image_data = data.get('image_data')
        mime_type = data.get('mime_type')
        language = data.get('language', 'en-US')
        
        if not all([image_data, mime_type]):
            return jsonify({'error': 'Image data and MIME type are required'}), 400
        
        if 'base64,' in image_data:
            image_data = image_data.split('base64,')[1]
        
        analysis_result = analyze_plant_image(image_data, mime_type, language)
        
        return jsonify({'analysis': analysis_result})
    
    except Exception as e:
        # THIS IS THE FIX: We are returning the EXACT error to the frontend
        return jsonify({'error': f'ACTUAL BUG: {str(e)}'}), 500
@ai_bp.route('/recommendations', methods=['GET'])
def get_recommendations():
    try:
        # FDE Failsafe: Bypass the missing frontend ID and use our local demo user
        from app.models.user import User
        from app.models.chat import Conversation, Message
        
        user = User.query.first()
        if not user:
            return jsonify({'error': 'No user found. Please start a chat first!'}), 404
        
        # Get user's conversations
        conversations = Conversation.query.filter_by(user_id=user.id).all()
        if not conversations:
            return jsonify({'error': 'No conversation history found to analyze.'}), 404
        
        # Extract chat history
        chat_history = ""
        for conv in conversations:
            messages = Message.query.filter_by(conversation_id=conv.id).order_by(Message.timestamp).all()
            for msg in messages:
                chat_history += f"{msg.sender}: {msg.content}\n"
            chat_history += "\n---\n\n"
        
        # Generate recommendations
        from app.services.ai_services import generate_recommendations
        recommendations = generate_recommendations(chat_history)
        
        return jsonify({'recommendations': recommendations})
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Failed to generate recommendations: {str(e)}'}), 500
    