from models.notification_model import NotificationModel

class NotificationController:

    @staticmethod
    def send(data):
        NotificationModel.send_notification(data)
        return {"success": True, "message": "Notification sent"}

    @staticmethod
    def list_notifications():
        data = NotificationModel.get_all_notifications()
        return {"success": True, "data": data}
