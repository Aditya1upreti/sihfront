# app/models/__init__.py

from app import db
from .user import User
from .chat import Conversation, Message

# This makes the models available when importing from app.models
__all__ = ['User', 'Conversation', 'Message']

def init_models(app):
    """
    Initialize models with the Flask app
    """
    with app.app_context():
        try:
            # Create all tables
            db.create_all()
            print("✅ Database tables initialized successfully")
        except Exception as e:
            print(f"❌ Error initializing database tables: {e}")
            raise

# Model relationships and additional setup can go here
def setup_relationships():
    """
    Setup any complex model relationships
    """
    # User-Conversation relationship (one-to-many)
    User.conversations = db.relationship(
        'Conversation', 
        backref='user', 
        lazy=True,
        cascade='all, delete-orphan'
    )
    
    # Conversation-Message relationship (one-to-many)
    Conversation.messages = db.relationship(
        'Message', 
        backref='conversation', 
        lazy=True,
        cascade='all, delete-orphan',
        order_by='Message.timestamp'
    )

# Utility functions for models
def get_or_create(session, model, **kwargs):
    """
    Get or create a model instance
    """
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance, True

def bulk_create(session, model, data_list):
    """
    Bulk create model instances
    """
    instances = [model(**data) for data in data_list]
    session.bulk_save_objects(instances)
    session.commit()
    return instances

print("✅ Models package initialized successfully")