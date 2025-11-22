from flask import Blueprint, jsonify
from controllers.superadmin_controller import SuperAdminController

superadmin_bp = Blueprint("superadmin_bp", __name__)


@superadmin_bp.get("/students")
def list_students():
    result = SuperAdminController.list_students()
    return jsonify(result)


@superadmin_bp.get("/admins")
def list_admins():
    result = SuperAdminController.list_admins()
    return jsonify(result)


@superadmin_bp.get("/attendance")
def all_attendance():
    result = SuperAdminController.all_attendance()
    return jsonify(result)
