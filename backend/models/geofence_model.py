from db import get_db_connection
from datetime import datetime, timedelta


class GeofenceModel:

    # ---------------------------------------------------------
    # CREATE GEOFENCE
    # ---------------------------------------------------------
    @staticmethod
    def create_geofence(data):
        conn = get_db_connection()
        cursor = conn.cursor()

        valid_minutes = int(data.get("valid_minutes", 0))

        # expires_at → NULL or datetime
        expires_at = None
        if valid_minutes > 0:
            expires_at = datetime.now() + timedelta(minutes=valid_minutes)

        query = """
            INSERT INTO geofence (landmark, latitude, longitude, radius, expires_at)
            VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(query, (
            data.get("landmark"),
            float(data.get("latitude")),
            float(data.get("longitude")),
            int(data.get("radius", 200)),
            expires_at
        ))

        geofence_id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()

        return geofence_id

    # ---------------------------------------------------------
    # ALL GEOFENCES + COUNT
    # ---------------------------------------------------------
    @staticmethod
    def get_all_geofences_with_count():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT 
                g.*,
                IFNULL((SELECT COUNT(*) FROM attendance a WHERE a.geofence_id = g.id), 0)
                    AS attendance_count
            FROM geofence g
            ORDER BY g.created_at DESC
        """)

        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        # Convert datetime
        for r in rows:
            if isinstance(r.get("created_at"), datetime):
                r["created_at"] = r["created_at"].isoformat()

            if isinstance(r.get("expires_at"), datetime):
                r["expires_at"] = r["expires_at"].isoformat()
            else:
                r["expires_at"] = None

        return rows

    # ---------------------------------------------------------
    # ACTIVE GEOFENCE (NOT EXPIRED)
    # USED BY STUDENTS + ADMINS
    # ---------------------------------------------------------
    @staticmethod
    def get_active_geofence():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT 
                g.*,
                IFNULL((SELECT COUNT(*) FROM attendance a WHERE a.geofence_id = g.id), 0)
                    AS attendance_count
            FROM geofence g
            WHERE g.expires_at IS NULL OR g.expires_at > NOW()
            ORDER BY g.created_at DESC
            LIMIT 1
        """)

        row = cursor.fetchone()

        cursor.close()
        conn.close()

        if not row:
            return None

        if isinstance(row.get("created_at"), datetime):
            row["created_at"] = row["created_at"].isoformat()

        if isinstance(row.get("expires_at"), datetime):
            row["expires_at"] = row["expires_at"].isoformat()
        else:
            row["expires_at"] = None

        return row

    # ---------------------------------------------------------
    # LATEST GEOFENCE (EVEN EXPIRED)
    # USED BY ADMIN IN SOME CASES
    # ---------------------------------------------------------
    @staticmethod
    def get_latest_geofence():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT 
                g.*,
                IFNULL((SELECT COUNT(*) FROM attendance a WHERE a.geofence_id = g.id), 0)
                    AS attendance_count
            FROM geofence g
            ORDER BY g.created_at DESC
            LIMIT 1
        """)

        row = cursor.fetchone()

        cursor.close()
        conn.close()

        if not row:
            return None

        if isinstance(row.get("created_at"), datetime):
            row["created_at"] = row["created_at"].isoformat()

        if isinstance(row.get("expires_at"), datetime):
            row["expires_at"] = row["expires_at"].isoformat()
        else:
            row["expires_at"] = None

        return row
