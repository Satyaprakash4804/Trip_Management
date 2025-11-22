from flask import Blueprint, request, jsonify
from controllers.student_controller import StudentController
from utils.jwt_helper import JWTHelper
from db import get_db_connection

student_bp = Blueprint("student_bp", __name__)


# ---------------------------------------------------------
# UTILITY — extract logged user from JWT cookie
# ---------------------------------------------------------
def get_logged_user():
    try:
        token = request.cookies.get("access_token")
        if not token:
            return None

        user, valid = JWTHelper.verify_token(token)
        return user if valid else None

    except Exception as e:
        print("❌ ERROR in get_logged_user():", e)
        return None


# ---------------------------------------------------------
# MARK ATTENDANCE (Option A)
# ---------------------------------------------------------
@student_bp.post("/mark_attendance")
def mark_attendance():
    try:
        user = get_logged_user()
        if not user:
            return jsonify({"success": False, "message": "Unauthorized"}), 401

        data = request.json or {}

        # Inject user_id into data dict
        data["user_id"] = user["id"]

        print("📌 Attendance Data:", data)

        result = StudentController.mark_attendance(data)
        return jsonify(result)

    except Exception as e:
        print("❌ ERROR in mark_attendance():", e)
        return jsonify({"success": False, "message": str(e)}), 500


# ---------------------------------------------------------
# UPLOAD PHOTO
# ---------------------------------------------------------
@student_bp.post("/upload")
def upload_photo():
    try:
        user = get_logged_user()
        if not user:
            return jsonify({"success": False, "message": "Unauthorized"}), 401

        file = request.files.get("file")
        desc = request.form.get("description")

        if not file:
            return jsonify({"success": False, "message": "No file selected"})

        filename = "uploads/student_uploads/" + file.filename
        file.save(filename)

        data = {
            "user_id": user["id"],
            "description": desc,
            "uploaded_by_role": "student",
            "file_path": filename
        }

        return jsonify(StudentController.upload_photo(data))

    except Exception as e:
        print("❌ ERROR in upload_photo():", e)
        return jsonify({"success": False, "message": str(e)}), 500


# ---------------------------------------------------------
# MY ATTENDANCE
# ---------------------------------------------------------
@student_bp.get("/my_attendance")
def my_attendance():
    try:
        user = get_logged_user()
        if not user:
            return jsonify({"success": False, "message": "Unauthorized"}), 401

        return jsonify(StudentController.my_attendance(user["id"]))

    except Exception as e:
        print("❌ ERROR in my_attendance():", e)
        return jsonify({"success": False, "message": str(e)}), 500


# ---------------------------------------------------------
# ACTIVE GEOFENCE CHECK
# ---------------------------------------------------------
@student_bp.get("/geofence_status")
def geofence_status():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT * FROM geofence
            WHERE expires_at IS NULL OR expires_at > NOW()
            ORDER BY id DESC LIMIT 1
        """)

        geo = cursor.fetchone()
        cursor.close()
        conn.close()

        if not geo:
            return jsonify({"enabled": False})

        return jsonify({"enabled": True, "geofence": geo})

    except Exception as e:
        print("❌ ERROR in geofence_status():", e)
        return jsonify({"enabled": False, "error": str(e)})
