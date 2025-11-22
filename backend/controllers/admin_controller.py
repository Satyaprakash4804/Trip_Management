from geopy.distance import geodesic
from models.upload_model import UploadModel
from models.attendance_model import AttendanceModel
from models.geofence_model import GeofenceModel


class AdminController:

    @staticmethod
    def mark_attendance(data):

        # Required fields
        required_fields = ["user_id", "role", "marked_lat", "marked_lng"]
        for field in required_fields:
            if field not in data:
                return {"success": False, "message": f"Missing field: {field}"}

        # Get latest geofence
        geofence = GeofenceModel.get_latest_geofence()
        if not geofence:
            return {"success": False, "message": "No geofence set by master"}

        # ----------------------------------
        # Validate mobile GPS coordinates
        # ----------------------------------
        try:
            marked_lat = float(data["marked_lat"])
            marked_lng = float(data["marked_lng"])
        except Exception:
            return {"success": False, "message": "Invalid or missing latitude/longitude"}

        marked_location = (marked_lat, marked_lng)

        # ----------------------------------
        # Load geofence coordinates correctly
        # ----------------------------------
        try:
            center_lat = float(geofence["latitude"])
            center_lng = float(geofence["longitude"])
            radius = float(geofence["radius"])  # meters
        except KeyError as e:
            return {"success": False, "message": f"Geofence key missing: {str(e)}"}

        geofence_center = (center_lat, center_lng)

        # ----------------------------------
        # Calculate distance in meters
        # ----------------------------------
        distance_meters = geodesic(marked_location, geofence_center).meters
        data["distance"] = round(distance_meters, 2)

        # Add geofence ID
        data["geofence_id"] = geofence["id"]

        # ----------------------------------
        # FINAL FIX: map status to your DB values
        # DB expects → "present" / "absent"
        # ----------------------------------
        if distance_meters <= radius:
            data["status"] = "present"
        else:
            data["status"] = "absent"

        # Save attendance
        AttendanceModel.mark_attendance(data)

        return {
            "success": True,
            "message": f"{data['role'].capitalize()} attendance marked successfully"
        }

    # -------------------------------------
    # PHOTO UPLOAD
    # -------------------------------------
    @staticmethod
    def upload_photo(data):
        UploadModel.save_upload(data)
        return {"success": True, "message": "Photo uploaded"}

    # -------------------------------------
    # STUDENT DETAILS
    # -------------------------------------
    @staticmethod
    def student_details():
        from models.user_model import UserModel
        students = UserModel.get_all_students()
        return {"success": True, "data": students}

    # -------------------------------------
    # ATTENDANCE DATA
    # -------------------------------------
    @staticmethod
    def attendance_data():

        students = AttendanceModel.get_attendance_for_role("student")
        admins = AttendanceModel.get_attendance_for_role("admin")

        return {
            "success": True,
            "students": students,
            "admins": admins
        }
