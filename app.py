import os
from flask import Flask
from flask_login import LoginManager
from models import db, User

def create_app():
    app = Flask(__name__)

    # ── Config ──────────────────────────────────────────────────────────────
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'pandemic-surveillance-secret-key-2024')
    
    database_url = os.environ.get('DATABASE_URL', 'sqlite:///pandemic_surveillance.db')
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # ── Extensions ───────────────────────────────────────────────────────────
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'warning'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # ── Blueprints ────────────────────────────────────────────────────────────
    from auth import auth_bp
    from admin import admin_bp
    from api import api_bp
    from routes import main_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(main_bp)

    # ── Create tables ─────────────────────────────────────────────────────────
    with app.app_context():
        db.create_all()

    return app


app = create_app()

if __name__ == '__main__':
    print("🦠  Pandemic Surveillance System running at http://127.0.0.1:5000")
    app.run(debug=True)
