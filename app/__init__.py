from flask import Flask, send_from_directory, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from config import Config
from .assets import get_room_images_dir, list_room_images


db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message_category = "warning"


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    @app.route("/assets/rooms/<path:filename>")
    def room_image_asset(filename: str):
        images_dir = get_room_images_dir()
        return send_from_directory(images_dir, filename)

    @app.context_processor
    def inject_image_helpers():
        placeholder_url = "https://placehold.co/640x360?text=Room"
        available_images = list_room_images()

        def room_image_url(filename: str | None = None) -> str:
            target = filename or (available_images[0] if available_images else None)
            if target:
                return url_for("room_image_asset", filename=target)
            return placeholder_url

        return {"room_image_url": room_image_url}

    with app.app_context():
        from . import models  # noqa: F401
        from .auth import bp as auth_bp
        from .user import bp as user_bp
        from .admin import bp as admin_bp
        from .landing import bp as landing_bp
        from .commands import register_commands

        register_commands(app)

        db.create_all()

        app.register_blueprint(landing_bp)
        app.register_blueprint(auth_bp)
        app.register_blueprint(user_bp)
        app.register_blueprint(admin_bp)

    return app
