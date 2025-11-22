from flask import Blueprint, request, jsonify
from controllers.admin_controller import AdminController
from models.geofence_model import GeofenceModel
from models.attendance_model import AttendanceModel

admin_bp = Blueprint("admin_bp", __name__)


# ----------------------- CHECK IF ADMIN CAN MARK ATTENDANCE -----------------------

@admin_bp.get("/check_attendance_status")
def check_attendance_status():
    from utils.jwt_helper import JWTHelper

    token = request.cookies.get("access_token")
    user, valid = JWTHelper.verify_token(token)

    if not valid:
        return jsonify({"allowed": False, "reason": "Not logged in"})

    user_id = user["id"]

    latest_geofence = GeofenceModel.get_latest_geofence()
    if not latest_geofence:
        return jsonify({"allowed": False, "reason": "Geofence not set"})

    last_att = AttendanceModel.get_latest_admin_attendance(user_id)

    # Never attended → allow
    if not last_att:
        return jsonify({"allowed": True})

    # If last attendance belongs to same geofence → block
    if last_att["geofence_id"] == latest_geofence["id"]:
        return jsonify({"allowed": False})

    return jsonify({"allowed": True})


@staticmethod
def mark_attendance(data):
    try:
        user_id = data.get("user_id")
        lat = float(data.get("marked_lat"))
        lng = float(data.get("marked_lng"))

        geofence = GeofenceModel.get_active_geofence()

        if not geofence:
            return {"success": False, "message": "No active geofence found"}

        from geopy.distance import geodesic
        distance = geodesic(
            (lat, lng),
            (geofence["latitude"], geofence["longitude"])
        ).meters

        if distance > geofence["radius"]:
            return {"success": False, "message": "You are outside geofence!"}

        AttendanceModel.mark_attendance({
            "user_id": user_id,
            "geofence_id": geofence["id"],
            "status": "present",
            "marked_lat": lat,
            "marked_lng": lng,
            "distance": distance
        })

        return {"success": True, "message": "Attendance marked"}
    
    except Exception as e:
        print("ERROR:", e)
        return {"success": False, "message": str(e)}



# ----------------------- UPLOAD FILE -----------------------
@admin_bp.post("/upload")
def upload():
    user_id = request.form.get("user_id")
    description = request.form.get("description")
    uploaded_by_role = "admin"

    file = request.files.get("file")
    filename = "uploads/admin_uploads/" + file.filename
    file.save(filename)

    data = {
        "user_id": user_id,
        "description": description,
        "uploaded_by_role": uploaded_by_role,
        "file_path": filename
    }

    result = AdminController.upload_photo(data)
    return jsonify(result)


# ----------------------- GET STUDENTS -----------------------
@admin_bp.get("/students")
def students():
    result = AdminController.student_details()
    return jsonify(result)


# ----------------------- GET ATTENDANCE RECORDS -----------------------
@admin_bp.get("/attendance")
def attendance():
    result = AdminController.attendance_data()
    return jsonify(result)
