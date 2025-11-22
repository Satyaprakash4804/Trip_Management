from db import get_db_connection


class AttendanceModel:

    # ---------------------------------------------------------
    # INSERT ATTENDANCE
    # ---------------------------------------------------------
    @staticmethod
    def mark_attendance(data):
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
            INSERT INTO attendance 
            (user_id, geofence_id, status, marked_lat, marked_lng, distance)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        cursor.execute(query, (
            data["user_id"],
            data["geofence_id"],
            data["status"],
            data["marked_lat"],
            data["marked_lng"],
            data["distance"]
        ))

        conn.commit()
        cursor.close()
        conn.close()
        return True

    # ---------------------------------------------------------
    # LAST ATTENDANCE OF ADMIN
    # ---------------------------------------------------------
    @staticmethod
    def get_latest_admin_attendance(user_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT 
                attendance.*,
                users.role
            FROM attendance
            JOIN users ON attendance.user_id = users.id
            WHERE attendance.user_id = %s
            ORDER BY attendance.id DESC LIMIT 1
        """, (user_id,))

        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result

    # ---------------------------------------------------------
    # GET ATTENDANCE FOR ROLE (admin or student)
    # ---------------------------------------------------------
    @staticmethod
    def get_attendance_for_role(role):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT 
                attendance.id,
                attendance.status,
                attendance.marked_lat,
                attendance.marked_lng,
                attendance.distance,
                attendance.timestamp,
                geofence.landmark,
                users.name,
                users.role
            FROM attendance
            JOIN users ON attendance.user_id = users.id
            LEFT JOIN geofence ON attendance.geofence_id = geofence.id
            WHERE users.role = %s
            ORDER BY attendance.timestamp DESC
        """, (role,))

        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result

    # ---------------------------------------------------------
    # GET FULL ATTENDANCE OF A SINGLE USER
    # ---------------------------------------------------------
    @staticmethod
    def get_user_attendance(user_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT 
                attendance.*,
                geofence.landmark,
                users.role
            FROM attendance
            LEFT JOIN geofence ON attendance.geofence_id = geofence.id
            JOIN users ON attendance.user_id = users.id
            WHERE attendance.user_id = %s
            ORDER BY attendance.timestamp DESC
        """, (user_id,))

        result = cursor.fetchall()
        cursor.close()
        conn.close()

        return result

    # ---------------------------------------------------------
    # CHECK IF USER ALREADY MARKED FOR SAME GEOFENCE
    # ---------------------------------------------------------
    @staticmethod
    def has_marked_attendance(user_id, geofence_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT id 
            FROM attendance
            WHERE user_id=%s AND geofence_id=%s
            LIMIT 1
        """, (user_id, geofence_id))

        result = cursor.fetchone()

        cursor.close()
        conn.close()

        return result is not None
