from db import get_db_connection

class UploadModel:

    @staticmethod
    def save_upload(data):
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
            INSERT INTO uploads (user_id, file_path, description, uploaded_by_role)
            VALUES (%s, %s, %s, %s)
        """

        cursor.execute(query, (
            data["user_id"],
            data["file_path"],
            data["description"],
            data["uploaded_by_role"]
        ))

        conn.commit()
        cursor.close()
        conn.close()
        return True

    @staticmethod
    def get_uploads():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT uploads.*, users.name
            FROM uploads
            LEFT JOIN users ON uploads.user_id = users.id
            ORDER BY uploads.timestamp DESC
        """)

        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result
