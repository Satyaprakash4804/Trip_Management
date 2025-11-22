from db import get_db_connection

class NotificationModel:

    @staticmethod
    def create_notification(data):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO notifications (title, message, send_to, sender_id)
            VALUES (%s, %s, %s, %s)
        """, (
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
    def list_notifications():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT n.*, u.name AS sender_name
            FROM notifications n
            LEFT JOIN users u ON u.id = n.sender_id
            ORDER BY n.id DESC
        """)

        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
