from flask import Blueprint, render_template, request, redirect
from utils.jwt_helper import JWTHelper

frontend_bp = Blueprint("frontend_bp", __name__)

# ------------------------------ SIDEBARS ------------------------------
SIDEBARS = {
    "master": [
        {"text": "Dashboard", "href": "/master/dashboard"},
        {"text": "Create Users", "href": "/master/create-users"},
        {"text": "Students", "href": "/master/students"},
        {"text": "Admins", "href": "/master/admins"},
        {"text": "Set Geofence", "href": "/master/geofence"},
        {"text": "Uploads", "href": "/master/uploads"},
        {"text": "Attendance", "href": "/master/attendance"},
        {"text": "Notifications", "href": "/notifications"}
    ],
    "super_admin": [
        {"text": "Dashboard", "href": "/superadmin/dashboard"},
        {"text": "Students", "href": "/superadmin/students"},
        {"text": "Admins", "href": "/superadmin/admins"},
        {"text": "Attendance", "href": "/superadmin/attendance"},
        {"text": "Notifications", "href": "/notifications"}
    ],
    "admin": [
        {"text": "Dashboard", "href": "/admin/dashboard"},
        {"text": "Mark Attendance", "href": "/admin/mark"},
        {"text": "Students", "href": "/admin/students"},
        {"text": "My Attendance", "href": "/admin/myattendance"},
        {"text": "Upload Photos", "href": "/admin/upload"},
        {"text": "Attendance Records", "href": "/admin/attendance"},
        {"text": "Notifications", "href": "/notifications"}
    ],
    "student": [
        {"text": "Dashboard", "href": "/student/dashboard"},
        {"text": "Mark Attendance", "href": "/student/mark"},
        {"text": "Upload Photo", "href": "/student/upload"},
        {"text": "My Attendance", "href": "/student/myattendance"},
        {"text": "Notifications", "href": "/notifications"}
    ]
}

# ------------------------------ LOGIN CHECK ------------------------------
def require_login(role=None):
    token = request.cookies.get("access_token")

    if not token:
        return None, redirect("/login")

    try:
        user, valid = JWTHelper.verify_token(token)
        if not valid:
            return None, redirect("/login")

        if role and user["role"] != role:
            return None, redirect("/login")

        return user, None

    except:
        return None, redirect("/login")


# ------------------------------ PUBLIC ROUTES ------------------------------
@frontend_bp.route("/")
def landing():
    return render_template("landing.html", sidebar=None)

@frontend_bp.route("/login")
def login_page():
    return render_template("login.html", sidebar=None)

@frontend_bp.route("/register/<int:user_id>")
def register_page(user_id):
    return render_template("register.html", user_id=user_id, sidebar=None)


# ------------------------------ MASTER PAGES ------------------------------
@frontend_bp.route("/master/dashboard")
def master_dashboard():
    user, error = require_login("master")
    if error: return error
    return render_template("master_dashboard.html", sidebar=SIDEBARS["master"])

@frontend_bp.route("/master/create-users")
def master_create_user():
    user, error = require_login("master")
    if error: return error
    return render_template("master_create_users.html", sidebar=SIDEBARS["master"])

@frontend_bp.route("/master/students")
def master_students():
    user, error = require_login("master")
    if error: return error
    return render_template("master_students.html", sidebar=SIDEBARS["master"])

@frontend_bp.route("/master/admins")
def master_admins():
    user, error = require_login("master")
    if error: return error
    return render_template("master_admins.html", sidebar=SIDEBARS["master"])

@frontend_bp.route("/master/geofence")
def master_geofence():
    user, error = require_login("master")
    if error: return error
    return render_template("master_geofence.html", sidebar=SIDEBARS["master"])

@frontend_bp.route("/master/uploads")
def master_uploads():
    user, error = require_login("master")
    if error: return error
    return render_template("view_uploads.html", sidebar=SIDEBARS["master"])

@frontend_bp.route("/master/attendance")
def master_attendance():
    user, error = require_login("master")
    if error: return error
    return render_template("attendance_table.html", sidebar=SIDEBARS["master"])

@frontend_bp.route("/attendance-on-map")
def attendance_on_map():
    token = request.cookies.get("access_token")

    sidebar = None
    if token:
        user, valid = JWTHelper.verify_token(token)
        if valid:
            sidebar = SIDEBARS.get(user["role"])

    return render_template("attendance_on_map.html", sidebar=sidebar)


# ------------------------------ SUPER ADMIN PAGES ------------------------------
@frontend_bp.route("/superadmin/dashboard")
def superadmin_dashboard():
    user, error = require_login("super_admin")
    if error: return error
    return render_template("superadmin_dashboard.html", sidebar=SIDEBARS["super_admin"])

@frontend_bp.route("/superadmin/students")
def superadmin_students():
    user, error = require_login("super_admin")
    if error: return error
    return render_template("superadmin_students.html", sidebar=SIDEBARS["super_admin"])

@frontend_bp.route("/superadmin/admins")
def superadmin_admins():
    user, error = require_login("super_admin")
    if error: return error
    return render_template("superadmin_admins.html", sidebar=SIDEBARS["super_admin"])

@frontend_bp.route("/superadmin/attendance")
def superadmin_attendance():
    user, error = require_login("super_admin")
    if error: return error
    return render_template("attendance_table.html", sidebar=SIDEBARS["super_admin"])


# ------------------------------ ADMIN PAGES ------------------------------
@frontend_bp.route("/admin/dashboard")
def admin_dashboard():
    user, error = require_login("admin")
    if error: return error
    return render_template("admin_dashboard.html", sidebar=SIDEBARS["admin"])

@frontend_bp.route("/admin/mark")
def admin_mark_attendance():
    user, error = require_login("admin")
    if error: return error
    return render_template("admin_mark.html", sidebar=SIDEBARS["admin"])

@frontend_bp.route("/admin/upload")
def admin_upload_page():
    user, error = require_login("admin")
    if error: return error
    return render_template("admin_upload.html", sidebar=SIDEBARS["admin"])

@frontend_bp.route("/admin/students")
def admin_students():
    user, error = require_login("admin")
    if error: return error
    return render_template("admin_students.html", sidebar=SIDEBARS["admin"])

@frontend_bp.route("/admin/myattendance")
def admin_myattendance():
    user, error = require_login("admin")
    if error: return error
    return render_template("admin_myattendance.html", sidebar=SIDEBARS["admin"])

@frontend_bp.route("/admin/attendance")
def admin_attendance_records():
    user, error = require_login("admin")
    if error: return error
    return render_template("attendance_table.html", sidebar=SIDEBARS["admin"])


# ------------------------------ STUDENT PAGES ------------------------------
@frontend_bp.route("/student/dashboard")
def student_dashboard():
    user, error = require_login("student")
    if error: return error
    return render_template("student_dashboard.html", sidebar=SIDEBARS["student"])

@frontend_bp.route("/student/mark")
def student_mark_attendance():
    user, error = require_login("student")
    if error: return error
    return render_template("student_mark.html", sidebar=SIDEBARS["student"])

@frontend_bp.route("/student/upload")
def student_upload():
    user, error = require_login("student")
    if error: return error
    return render_template("student_upload.html", sidebar=SIDEBARS["student"])

@frontend_bp.route("/student/myattendance")
def student_myattendance():
    user, error = require_login("student")
    if error: return error
    return render_template("student_myattendance.html", sidebar=SIDEBARS["student"])


# ------------------------------ NOTIFICATIONS PAGE ------------------------------
@frontend_bp.route("/notifications")
def notifications():
    token = request.cookies.get("access_token")
    sidebar = None

    if token:
        user, valid = JWTHelper.verify_token(token)
        if valid:
            sidebar = SIDEBARS.get(user["role"])

    return render_template("notifications.html", sidebar=sidebar)
