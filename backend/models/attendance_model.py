from db import get_db_connection
from utils.time_helper import now_ist
import pytz


class AttendanceModel:

    # ---------------------------------------------------------
    # HELPER → Convert UTC → IST safely
    # ---------------------------------------------------------
    @staticmethod
    def to_ist(ts):
        if ts is None:
            return None
        try:
            utc = pytz.utc.localize(ts)
        except Exception:
            return str(ts)

        ist = utc.astimezone(pytz.timezone("Asia/Kolkata"))
        return ist.strftime("%Y-%m-%d %H:%M:%S")

    # ---------------------------------------------------------
    # INSERT ATTENDANCE
    # ---------------------------------------------------------
    @staticmethod
    def mark_attendance(data):
        conn = get_db_connection()
        cursor = conn.cursor()

        timestamp = now_ist()  # IST timestamp

        query = """
            INSERT INTO attendance 
            (user_id, geofence_id, status, marked_lat, marked_lng, distance, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(query, (
            data["user_id"],
            data["geofence_id"],
            data["status"],
            data["marked_lat"],
            data["marked_lng"],
            data["distance"],
            timestamp
        ))

        conn.commit()
        cursor.close()
        conn.close()
        return True

    # ---------------------------------------------------------
    # CHECK DUPLICATE ATTENDANCE FOR SAME GEOFENCE
    # ---------------------------------------------------------
    @staticmethod
    def has_marked_attendance(user_id, geofence_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT id FROM attendance
            WHERE user_id=%s AND geofence_id=%s
            LIMIT 1
        """, (user_id, geofence_id))

        result = cursor.fetchone()

        cursor.close()
        conn.close()

        return result is not None

    # ---------------------------------------------------------
    # GET LAST ATTENDANCE OF ADMIN
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

        if result and result.get("timestamp"):
            result["timestamp"] = AttendanceModel.to_ist(result["timestamp"])

        return result

    # ---------------------------------------------------------
    # GET ATTENDANCE LIST BY ROLE (student/admin)
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

        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        # Convert timestamps → IST
        for r in rows:
            if r.get("timestamp"):
                r["timestamp"] = AttendanceModel.to_ist(r["timestamp"])

        return rows

    # ---------------------------------------------------------
    # FULL ATTENDANCE OF A SINGLE USER
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

        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        # Convert timestamp → IST
        for r in rows:
            if r.get("timestamp"):
                r["timestamp"] = AttendanceModel.to_ist(r["timestamp"])

        return rows
