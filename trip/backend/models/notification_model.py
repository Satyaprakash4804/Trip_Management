from db import get_db_connection

class NotificationModel:

    @staticmethod
    def send_notification(data):
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
            INSERT INTO notifications (title, message, send_to, sender_id)
            VALUES (%s, %s, %s, %s)
        """

        cursor.execute(query, (
            data["title"],
            data["message"],
            data["send_to"],
            data["sender_id"]
        ))

        conn.commit()
        cursor.close()
        conn.close()
        return True

    @staticmethod
    def get_all_notifications():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT notifications.*, users.name AS sender_name
            FROM notifications
            LEFT JOIN users ON notifications.sender_id = users.id
            ORDER BY notifications.timestamp DESC
        """)

        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result
