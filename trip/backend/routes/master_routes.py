from flask import Blueprint, request, jsonify
from models.user_model import UserModel
from controllers.master_controller import MasterController

master_bp = Blueprint("master_bp", __name__)


# ---------------------------------------------------------
# CREATE USER (ONLY: username, password, role)
# ---------------------------------------------------------
@master_bp.post("/create_user")
def create_user():
    data = request.json

    username = data.get("username")
    password = data.get("password")
    role = data.get("role")

    if not username or not password or not role:
        return jsonify({
            "success": False,
            "message": "Username, Password & Role are required"
        })

    user_data = {
        "username": username,
        "password": password,
        "role": role,
        "name": None,
        "email": None,
        "mobile": None,
        "college_id": None,
        "selfie": None,
        "aadhar_student": None,
        "aadhar_parent": None,
        "health_issue": None,
        "suggestions": None,
        "is_verified": 0
    }

    UserModel.create_user(user_data)

    return jsonify({
        "success": True,
        "message": f"{role.capitalize()} created successfully"
    })


# ---------------------------------------------------------
# LIST STUDENTS
# ---------------------------------------------------------
@master_bp.get("/students")
def list_students():
    return jsonify(MasterController.list_students())


# ---------------------------------------------------------
# LIST ADMINS
# ---------------------------------------------------------
@master_bp.get("/admins")
def list_admins():
    return jsonify(MasterController.list_admins())


# ---------------------------------------------------------
# DELETE USER
# ---------------------------------------------------------
@master_bp.delete("/delete/<int:user_id>")
def delete_user(user_id):
    return jsonify(MasterController.delete_user(user_id))


# ---------------------------------------------------------
# SET GEOFENCE
# ---------------------------------------------------------
@master_bp.post("/set_geofence")
def set_geofence():
    """
    Expected JSON:
    {
      "landmark": "Main Gate",
      "latitude": 26.85,
      "longitude": 80.95,
      "radius": 200,
      "valid_minutes": 60
    }
    """
    data = request.json
    result = MasterController.set_geofence(data)
    return jsonify(result)


# ---------------------------------------------------------
# GEOFENCE HISTORY
# ---------------------------------------------------------
@master_bp.get("/geofences")
def geofence_history():
    return jsonify(MasterController.get_geofence_history())


# ---------------------------------------------------------
# ACTIVE GEOFENCE
# ---------------------------------------------------------
@master_bp.get("/active_geofence")
def get_active_geofence():
    active = MasterController.get_active_geofence()
    return jsonify(active)


# ---------------------------------------------------------
# ALL UPLOADS
# ---------------------------------------------------------
@master_bp.get("/uploads")
def all_uploads():
    return jsonify(MasterController.get_all_uploads())


# ---------------------------------------------------------
# ATTENDANCE RECORDS
# ---------------------------------------------------------
@master_bp.get("/attendance")
def fetch_attendance():
    return jsonify(MasterController.get_attendance())


# ---------------------------------------------------------
# EDIT USER (MASTER)
# ---------------------------------------------------------
@master_bp.post("/edit/<int:user_id>")
def edit_user(user_id):
    data = request.json
    return jsonify(MasterController.edit_user(user_id, data))


@master_bp.put("/update_user/<int:user_id>")
def update_user(user_id):
    try:
        data = request.json
        result = MasterController.edit_user(user_id, data)
        return jsonify(result)
    except Exception as e:
        print("❌ ERROR in update_user():", e)
        return jsonify({"success": False, "message": str(e)}), 500
