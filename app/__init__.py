"""
DeadlineOS — Application Factory
Author (Backend): Nishant Kumar
"""

import os
from flask import Flask
from dotenv import load_dotenv
from app.extensions import login_manager
from app.routes.auth import auth_bp
from app.routes.dashboard import dashboard_bp
from app.routes.announcements import announcements_bp
from app.routes.deadlines import deadlines_bp
from app.routes.admin import admin_bp

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-key")

    # ── Initialize extensions ──────────────────────────────────────────────
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    # ── Register blueprints ────────────────────────────────────────────────
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(dashboard_bp, url_prefix="/")
    app.register_blueprint(announcements_bp, url_prefix="/announcements")
    app.register_blueprint(deadlines_bp, url_prefix="/deadlines")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    return app
