# run.py
from app import create_app
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = create_app()

if __name__ == '__main__':
    # Get configuration from environment
    host = os.environ.get('APP_HOST', '0.0.0.0')
    port = int(os.environ.get('APP_PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    print(f"🚀 Starting {os.environ.get('APP_NAME', 'Krish-Sahayak')} v{os.environ.get('APP_VERSION', '1.0.0')}")
    print(f"🌐 Server running on http://{host}:{port}")
    print(f"🔧 Debug mode: {debug}")
    print(f"⚙️  Environment: {os.environ.get('FLASK_ENV', 'development')}")
    
    # Run the application
    app.run(
        host=host,
        port=port,
        debug=debug,
        threaded=True
    )

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)