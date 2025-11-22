from flask import Blueprint, request, jsonify
from controllers.notification_controller import NotificationController
from utils.jwt_helper import JWTHelper

notification_bp = Blueprint("notification_bp", __name__)

def get_logged_user():
    token = request.cookies.get("access_token")
    if not token:
        return None
    user, valid = JWTHelper.verify_token(token)
    return user if valid else None


@notification_bp.post("/send")
def send_notification():
    user = get_logged_user()
    if not user:
        return jsonify({"success": False, "message": "Unauthorized"}), 401

    data = request.json
    data["sender_id"] = user["id"]

    return jsonify(NotificationController.send_notification(data))


@notification_bp.get("/list")
def list_notification():
    return jsonify(NotificationController.list_notifications())
