from models.user_model import UserModel
from models.attendance_model import AttendanceModel

class SuperAdminController:

    @staticmethod
    def list_students():
        data = UserModel.get_all_students()
        return {"success": True, "data": data}

    @staticmethod
    def list_admins():
        data = UserModel.get_all_admins()
        return {"success": True, "data": data}

    @staticmethod
    def all_attendance():
        student_att = AttendanceModel.get_attendance_for_role("student")
        admin_att = AttendanceModel.get_attendance_for_role("admin")

        return {
            "success": True,
            "students": student_att,
            "admins": admin_att
        }
