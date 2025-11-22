from models.user_model import UserModel
from models.geofence_model import GeofenceModel
from models.upload_model import UploadModel
from models.attendance_model import AttendanceModel


class MasterController:

    # ---------------------------------------------------------
    # CREATE USER
    # ---------------------------------------------------------
    @staticmethod
    def create_user(data):
        try:
            clean_data = {
                "username": data.get("username"),
                "password": data.get("password"),
                "role": data.get("role"),

                "name": None,
                "email": None,
                "mobile": None,
                "college_id": None,

                "selfie": None,
                "college_id_card": None,
                "aadhar_student": None,
                "aadhar_parent": None,
                "health_issue": None,

                "is_verified": 0
            }

            UserModel.create_user(clean_data)

            return {
                "success": True,
                "message": f"{data.get('role').capitalize()} created successfully"
            }

        except Exception as e:
            print("❌ ERROR in MasterController.create_user:", e)
            return {"success": False, "message": str(e)}

    # ---------------------------------------------------------
    # LIST STUDENTS
    # ---------------------------------------------------------
    @staticmethod
    def list_students():
        try:
            students = UserModel.get_all_students()
            return {"success": True, "data": students}
        except Exception as e:
            print("❌ ERROR in list_students:", e)
            return {"success": False, "data": []}

    # ---------------------------------------------------------
    # LIST ADMINS
    # ---------------------------------------------------------
    @staticmethod
    def list_admins():
        try:
            admins = UserModel.get_all_admins()
            return {"success": True, "data": admins}
        except Exception as e:
            print("❌ ERROR in list_admins:", e)
            return {"success": False, "data": []}

    # ---------------------------------------------------------
    # DELETE USER
    # ---------------------------------------------------------
    @staticmethod
    def delete_user(user_id):
        try:
            UserModel.delete_user(user_id)
            return {"success": True, "message": "User deleted successfully"}
        except Exception as e:
            print("❌ ERROR in delete_user:", e)
            return {"success": False, "message": str(e)}

    # ---------------------------------------------------------
    # EDIT USER
    # ---------------------------------------------------------
    @staticmethod
    def edit_user(user_id, data):
        try:
            UserModel.update_user_by_master(user_id, data)
            return {"success": True, "message": "User updated successfully"}
        except Exception as e:
            print("❌ ERROR in edit_user:", e)
            return {"success": False, "message": str(e)}

    # ---------------------------------------------------------
    # SET GEOFENCE
    # ---------------------------------------------------------
    @staticmethod
    def set_geofence(data):
        try:
            GeofenceModel.create_geofence(data)
            return {"success": True, "message": "Geofence created successfully"}
        except Exception as e:
            print("❌ ERROR in set_geofence:", e)
            return {"success": False, "message": str(e)}

    # ---------------------------------------------------------
    # GEOFENCE HISTORY
    # ---------------------------------------------------------
    @staticmethod
    def get_geofence_history():
        try:
            data = GeofenceModel.get_all_geofences_with_count()
            return {"success": True, "data": data}
        except Exception as e:
            print("❌ ERROR in get_geofence_history:", e)
            return {"success": False, "data": []}

    # ---------------------------------------------------------
    # ACTIVE GEOFENCE
    # ---------------------------------------------------------
    @staticmethod
    def get_active_geofence():
        try:
            data = GeofenceModel.get_active_geofence()
            return {"success": True, "data": data}
        except Exception as e:
            print("❌ ERROR in get_active_geofence:", e)
            return {"success": False, "data": None}

    # ---------------------------------------------------------
    # ALL UPLOADS
    # ---------------------------------------------------------
    @staticmethod
    def get_all_uploads():
        try:
            uploads = UploadModel.get_uploads()
            return {"success": True, "data": uploads}
        except Exception as e:
            print("❌ ERROR in get_all_uploads:", e)
            return {"success": False, "data": []}

    # ---------------------------------------------------------
    # ATTENDANCE
    # ---------------------------------------------------------
    @staticmethod
    def get_attendance():
        try:
            students = AttendanceModel.get_attendance_for_role("student")
            admins = AttendanceModel.get_attendance_for_role("admin")

            return {
                "success": True,
                "students": students,
                "admins": admins
            }

        except Exception as e:
            print("❌ ERROR in get_attendance:", e)
            return {
                "success": False,
                "students": [],
                "admins": []
            }
