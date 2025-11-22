from models.notification_model import NotificationModel

class NotificationController:

    @staticmethod
    def send_notification(data):
        NotificationModel.create_notification(data)
        return {"success": True, "message": "Notification sent!"}

    @staticmethod
    def list_notifications():
        rows = NotificationModel.list_notifications()
        return {"success": True, "data": rows}
