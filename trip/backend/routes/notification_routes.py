from flask import Blueprint, request, jsonify
from controllers.notification_controller import NotificationController

notification_bp = Blueprint("notification_bp", __name__)


@notification_bp.post("/send")
def send_notification():
    data = request.json
    result = NotificationController.send(data)
    return jsonify(result)


@notification_bp.get("/list")
def list_notifications():
    result = NotificationController.list_notifications()
    return jsonify(result)
