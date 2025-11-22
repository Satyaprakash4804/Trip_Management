from models.upload_model import UploadModel
from models.attendance_model import AttendanceModel
from models.geofence_model import GeofenceModel

class AdminController:

    @staticmethod
    def mark_attendance(data):
        geofence = GeofenceModel.get_latest_geofence()
        if not geofence:
            return {"success": False, "message": "No geofence set by master"}

        AttendanceModel.mark_attendance(data)
        return {"success": True, "message": "Attendance marked"}

    @staticmethod
    def upload_photo(data):
        UploadModel.save_upload(data)
        return {"success": True, "message": "Photo uploaded"}

    @staticmethod
    def student_details():
        from models.user_model import UserModel
        students = UserModel.get_all_students()
        return {"success": True, "data": students}

    @staticmethod
    def attendance_data():
        data = AttendanceModel.get_attendance_for_role("student")
        return {"success": True, "data": data}
