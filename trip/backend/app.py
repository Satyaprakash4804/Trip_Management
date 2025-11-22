from dotenv import load_dotenv
import os

ROOT_ENV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(ROOT_ENV_PATH)

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # CORS FIX for JWT Cookies
    CORS(
        app,
        supports_credentials=True,
        resources={r"/*": {"origins": "*"}}
    )

    # Create required upload directories
    upload_folders = [
        "uploads", 
        "uploads/selfies", 
        "uploads/aadhar_student",
        "uploads/aadhar_parent", 
        "uploads/admin_uploads",
        "uploads/student_uploads",
        "uploads/college_id"
    ]
    for folder in upload_folders:
        os.makedirs(folder, exist_ok=True)

    # Blueprints
    from routes.frontend_routes import frontend_bp
    from routes.auth_routes import auth_bp
    from routes.master_routes import master_bp
    from routes.admin_routes import admin_bp
    from routes.student_routes import student_bp
    from routes.superadmin_routes import superadmin_bp
    from routes.notification_routes import notification_bp

    app.register_blueprint(frontend_bp)
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(master_bp, url_prefix="/api/master")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")
    app.register_blueprint(student_bp, url_prefix="/api/student")
    app.register_blueprint(superadmin_bp, url_prefix="/api/superadmin")
    app.register_blueprint(notification_bp, url_prefix="/api/notifications")

    # FIXED — SERVE ALL NESTED FILES
    @app.route('/uploads/<path:path>')
    def serve_uploads(path):
        return send_from_directory("uploads", path)

    @app.errorhandler(413)
    def request_entity_too_large(e):
        return jsonify({
            "success": False,
            "message": f"File too large. Max allowed size is {Config.MAX_CONTENT_LENGTH} bytes"
        }), 413

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)
