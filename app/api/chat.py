from flask import Blueprint, request, jsonify
from app.models.chat import Conversation, Message
# No longer need the User model directly here for lookups, as the decorator handles it.
from app import db
from app.services.ai_services import get_ai_response, generate_chat_title
from datetime import datetime
# Import the decorator from your auth file
from app.api.auth import token_required

chat_bp = Blueprint('chat', __name__, url_prefix='/api/chat')

# The get_or_create_user helper function is no longer needed and can be removed,
# as authentication is now handled by the @token_required decorator.

@chat_bp.route('/conversations', methods=['GET'])
@token_required
def get_conversations(current_user):
    """Gets all conversations for the logged-in user."""
    try:
        # The user is now provided by the @token_required decorator
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
        return jsonify({'error': 'Failed to retrieve conversations'}), 500

@chat_bp.route('/conversations', methods=['POST'])
@token_required
def create_conversation(current_user):
    """Creates a new conversation for the logged-in user."""
    try:
        data = request.get_json()
        language = data.get('lang')
        welcome_message = data.get('welcomeMessage')
        
        if not all([language, welcome_message]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Use the current_user's id provided by the decorator
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
        db.session.rollback()
        return jsonify({'error': 'Failed to create conversation'}), 500

@chat_bp.route('/conversations/<int:conversation_id>', methods=['DELETE'])
@token_required
def delete_conversation(current_user, conversation_id):
    """Deletes a specific conversation for the logged-in user."""
    try:
        # Ensure the conversation belongs to the current user
        conversation = Conversation.query.filter_by(id=conversation_id, user_id=current_user.id).first()
        
        if not conversation:
            return jsonify({'error': 'Conversation not found or access denied'}), 404
        
        Message.query.filter_by(conversation_id=conversation_id).delete()
        db.session.delete(conversation)
        db.session.commit()
        
        return jsonify({'success': True})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete conversation'}), 500

@chat_bp.route('/conversations', methods=['DELETE'])
@token_required
def delete_all_conversations(current_user):
    """Deletes all conversations for the logged-in user."""
    try:
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
@token_required
def send_message(current_user, conversation_id):
    """Sends a message in a conversation belonging to the logged-in user."""
    try:
        data = request.get_json()
        prompt = data.get('prompt')
        
        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400
        
        # Ensure the conversation belongs to the current user
        conversation = Conversation.query.filter_by(id=conversation_id, user_id=current_user.id).first()
        
        if not conversation:
            return jsonify({'error': 'Conversation not found or access denied'}), 404
        
        user_message = Message(
            conversation_id=conversation.id,
            sender='user',
            content=prompt,
            timestamp=datetime.utcnow()
        )
        db.session.add(user_message)
        
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
        return jsonify({'error': 'Failed to process message'}), 500
