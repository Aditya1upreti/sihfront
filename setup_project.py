# setup_project.py
import os
import subprocess
import sys

def check_python():
    """Check if Python is available"""
    try:
        subprocess.run([sys.executable, "--version"], check=True, capture_output=True)
        return True
    except:
        print("❌ Python is not available. Please install Python 3.7+")
        return False

def create_virtual_env():
    """Create virtual environment"""
    if not os.path.exists(".venv"):
        print("📦 Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", ".venv"], check=True)
        print("✅ Virtual environment created")
    else:
        print("✅ Virtual environment already exists")

def install_requirements():
    """Install required packages"""
    if os.path.exists("requirements.txt"):
        print("📦 Installing requirements...")
        
        # Use the virtual environment's pip
        if os.name == 'nt':  # Windows
            pip_path = os.path.join(".venv", "Scripts", "pip")
        else:  # Mac/Linux
            pip_path = os.path.join(".venv", "bin", "pip")
        
        subprocess.run([pip_path, "install", "-r", "requirements.txt"], check=True)
        print("✅ Requirements installed")
    else:
        print("❌ requirements.txt not found")

def create_env_file():
    """Create .env file"""
    env_content = """# =============================================
# KRISH-SAHAYAK - AGRICULTURAL ASSISTANT
# =============================================

# Flask Application Settings
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=krish-sahayak-secret-key-2024-change-in-production

# Database Configuration
DATABASE_URL=sqlite:///agri_assistant.db

# JWT Authentication
JWT_SECRET=your-jwt-secret-key-for-krish-sahayak-make-this-very-long
JWT_EXPIRATION_HOURS=24

# Gemini AI API
GEMINI_API_KEY=AIzaSyA0JQMrzRv_Gw_Wr_ekGSG73v_Xl5T--SU

# Application Configuration
APP_NAME=Krish-Sahayak
APP_VERSION=1.0.0
APP_PORT=5000
APP_HOST=0.0.0.0

# CORS Settings
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,http://localhost:5000

# File Upload Limits
MAX_FILE_SIZE=16777216

# Default Settings for Kerala
DEFAULT_STATE=Kerala
DEFAULT_LANGUAGE=en

# Feature Flags
WEATHER_FEATURE_ENABLED=true
MARKET_PRICES_FEATURE_ENABLED=true
GRIEVANCES_FEATURE_ENABLED=true
SUBSIDIES_FEATURE_ENABLED=true
GOVT_SCHEMES_FEATURE_ENABLED=true
CHAT_FEATURE_ENABLED=true
PLANT_ID_FEATURE_ENABLED=true

# Logging
LOG_LEVEL=INFO
"""

    with open('.env', 'w') as f:
        f.write(env_content)
    print("✅ .env file created")

def setup_database():
    """Initialize database"""
    try:
        # Set environment variables for Flask
        env = os.environ.copy()
        env['FLASK_APP'] = 'run.py'
        env['FLASK_ENV'] = 'development'
        
        print("🗄️  Initializing database...")
        subprocess.run(['flask', 'db', 'init'], env=env, check=True)
        subprocess.run(['flask', 'db', 'migrate', '-m', 'Initial setup'], env=env, check=True)
        subprocess.run(['flask', 'db', 'upgrade'], env=env, check=True)
        print("✅ Database initialized")
    except Exception as e:
        print(f"❌ Database setup failed: {e}")

def main():
    print("🚀 Krish-Sahayak Project Setup")
    print("=" * 40)
    
    if not check_python():
        return
    
    create_virtual_env()
    install_requirements()
    create_env_file()
    setup_database()
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Activate virtual environment:")
    print("   Windows: .venv\\Scripts\\activate")
    print("   Mac/Linux: source .venv/bin/activate")
    print("2. Run the application: python run.py")
    print("3. Open http://localhost:5000 in your browser")

if __name__ == "__main__":
    main()