from flask import Blueprint, request, jsonify
from app.models.chat import Conversation, Message
from app.models.user import User
from app import db
from app.services.ai_services import get_ai_response, generate_chat_title
from datetime import datetime
import uuid

# FIX 1: Removed the double '/api' prefix
chat_bp = Blueprint('chat', __name__, url_prefix='/chat')

# FIX 2: Local Demo Helper - Bypasses JWT and automatically assigns chats to a demo user
def get_current_user():
    user = User.query.first()
    if not user:
        user = User(uuid=str(uuid.uuid4()), email="demo@example.com")
        db.session.add(user)
        db.session.commit()
    return user

@chat_bp.route('/conversations', methods=['GET'])
def get_conversations():
    """Gets all conversations for the demo user."""
    try:
        current_user = get_current_user()
        conversations = Conversation.query.filter_by(user_id=current_user.id).order_by(Conversation.created_at.desc()).all()
        
        result = []
        for conv in conversations:
            result.append({
                'id': conv.id,
                'title': conv.title,
                'language': conv.language,
                'createdAt': conv.created_at.isoformat(),
                'messages': [{
                    'sender': msg.sender,
                    'text': msg.content,
                    'timestamp': msg.timestamp.isoformat()
                } for msg in conv.messages]
            })
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': f'Failed to retrieve conversations: {str(e)}'}), 500

@chat_bp.route('/conversations', methods=['POST'])
def create_conversation():
    """Creates a new conversation."""
    try:
        current_user = get_current_user()
        data = request.get_json()
        
        # FIX 3: Matched the exact keys the frontend JavaScript is sending
        language = data.get('language')
        welcome_message = data.get('initial_message')
        
        if not all([language, welcome_message]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        conversation = Conversation(
            user_id=current_user.id,
            title='New Chat' if language == 'en-US' else 'പുതിയ ചാറ്റ്',
            language=language,
            created_at=datetime.utcnow()
        )
        db.session.add(conversation)
        db.session.flush()
        
        welcome_msg = Message(
            conversation_id=conversation.id,
            sender='ai',
            content=welcome_message,
            timestamp=datetime.utcnow()
        )
        db.session.add(welcome_msg)
        db.session.commit()
        
        return jsonify({
            'id': conversation.id,
            'title': conversation.title,
            'language': conversation.language,
            'createdAt': conversation.created_at.isoformat(),
            'messages': [{'sender': 'ai', 'text': welcome_message}]
        }), 201
    
    except Exception as e:
        import traceback
        traceback.print_exc()  # 🔥 THIS PRINTS THE EXACT RED ERROR TO YOUR TERMINAL
        db.session.rollback()
        return jsonify({'error': f'Failed to create conversation: {str(e)}'}), 500

@chat_bp.route('/conversations/<int:conversation_id>', methods=['DELETE'])
def delete_conversation(conversation_id):
    """Deletes a specific conversation."""
    try:
        current_user = get_current_user()
        conversation = Conversation.query.filter_by(id=conversation_id, user_id=current_user.id).first()
        
        if not conversation:
            return jsonify({'error': 'Conversation not found'}), 404
        
        Message.query.filter_by(conversation_id=conversation_id).delete()
        db.session.delete(conversation)
        db.session.commit()
        
        return jsonify({'success': True})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete conversation'}), 500

@chat_bp.route('/conversations', methods=['DELETE'])
def delete_all_conversations():
    """Deletes all conversations."""
    try:
        current_user = get_current_user()
        conversations = Conversation.query.filter_by(user_id=current_user.id).all()
        for conv in conversations:
            Message.query.filter_by(conversation_id=conv.id).delete()
            db.session.delete(conv)
        
        db.session.commit()
        return jsonify({'success': True})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete all conversations'}), 500

@chat_bp.route('/conversations/<int:conversation_id>/messages', methods=['POST'])
def send_message(conversation_id):
    """Sends a message to the AI."""
    try:
        current_user = get_current_user()
        data = request.get_json()
        
        # FIX 4: Frontend sends "message", not "prompt"
        prompt = data.get('message') 
        
        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400
        
        conversation = Conversation.query.filter_by(id=conversation_id, user_id=current_user.id).first()
        
        if not conversation:
            return jsonify({'error': 'Conversation not found'}), 404
        
        user_message = Message(
            conversation_id=conversation.id,
            sender='user',
            content=prompt,
            timestamp=datetime.utcnow()
        )
        db.session.add(user_message)
        
        # Call the Gemini AI
        ai_response_text = get_ai_response(conversation, prompt)
        
        ai_message = Message(
            conversation_id=conversation.id,
            sender='ai',
            content=ai_response_text,
            timestamp=datetime.utcnow()
        )
        db.session.add(ai_message)
        
        if conversation.title in ['New Chat', 'പുതിയ ചാറ്റ്']:
            new_title = generate_chat_title(prompt)
            if new_title:
                conversation.title = new_title
        
        db.session.commit()
        
        updated_messages = Message.query.filter_by(conversation_id=conversation.id).order_by(Message.timestamp).all()
        
        return jsonify({
            'aiResponse': {'text': ai_response_text},
            'updatedChat': {
                'id': conversation.id,
                'title': conversation.title,
                'language': conversation.language,
                'createdAt': conversation.created_at.isoformat(),
                'messages': [{
                    'sender': msg.sender,
                    'text': msg.content
                } for msg in updated_messages]
            }
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to process message: {str(e)}'}), 500