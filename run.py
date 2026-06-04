import os
from app import create_app
from dotenv import load_dotenv

# 1. Load local .env (Render will ignore this and use the variables you typed in their dashboard)
load_dotenv()

# 2. Create the app instance (Gunicorn looks for this 'app' variable!)
app = create_app()

if __name__ == '__main__':
    # 3. Use the PORT provided by Render, or default to 5000 for local development
    port = int(os.environ.get("PORT", 5000))
    
    # 4. In production, 'debug' should usually be False
    app.run(host='0.0.0.0', port=port, debug=True)