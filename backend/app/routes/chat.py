from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.chat import ChatSession, ChatMessage
from ..models.user import User
from .. import db
from datetime import datetime

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/session', methods=['POST'])
@jwt_required()
def create_session():
    user_id = get_jwt_identity()
    
    # Create new chat session
    session = ChatSession(user_id=user_id)
    db.session.add(session)
    db.session.commit()
    
    return jsonify({
        'session_id': session.id,
        'started_at': session.started_at.isoformat()
    }), 201

@chat_bp.route('/message', methods=['POST'])
@jwt_required()
def send_message():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not all(k in data for k in ['session_id', 'content']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    session = ChatSession.query.get(data['session_id'])
    if not session or session.user_id != user_id:
        return jsonify({'error': 'Invalid session'}), 404
    
    # Save user message
    user_message = ChatMessage(
        session_id=session.id,
        content=data['content'],
        is_bot=False
    )
    db.session.add(user_message)
    
    # Generate bot response (simplified for now)
    bot_response = generate_bot_response(data['content'])
    bot_message = ChatMessage(
        session_id=session.id,
        content=bot_response,
        is_bot=True
    )
    db.session.add(bot_message)
    
    session.update_activity()
    db.session.commit()
    
    return jsonify({
        'user_message': user_message.content,
        'bot_response': bot_message.content,
        'timestamp': bot_message.timestamp.isoformat()
    }), 200

@chat_bp.route('/history/<int:session_id>', methods=['GET'])
@jwt_required()
def get_history(session_id):
    user_id = get_jwt_identity()
    
    session = ChatSession.query.get(session_id)
    if not session or session.user_id != user_id:
        return jsonify({'error': 'Invalid session'}), 404
    
    messages = ChatMessage.query.filter_by(session_id=session_id).order_by(ChatMessage.timestamp).all()
    
    return jsonify({
        'session_id': session_id,
        'messages': [{
            'content': msg.content,
            'is_bot': msg.is_bot,
            'timestamp': msg.timestamp.isoformat()
        } for msg in messages]
    }), 200

@chat_bp.route('/reset/<int:session_id>', methods=['POST'])
@jwt_required()
def reset_session(session_id):
    user_id = get_jwt_identity()
    
    session = ChatSession.query.get(session_id)
    if not session or session.user_id != user_id:
        return jsonify({'error': 'Invalid session'}), 404
    
    # Delete all messages in the session
    ChatMessage.query.filter_by(session_id=session_id).delete()
    
    # Create new session
    new_session = ChatSession(user_id=user_id)
    db.session.add(new_session)
    db.session.commit()
    
    return jsonify({
        'message': 'Session reset successfully',
        'new_session_id': new_session.id
    }), 200

def generate_bot_response(user_message):
    """
    Simple bot response generation (to be enhanced with actual NLP/ML)
    """
    # This is a placeholder - in a real implementation, this would use
    # NLP/ML to generate appropriate responses based on the user's message
    return f"I received your message: {user_message}. How can I help you with your shopping needs?" 