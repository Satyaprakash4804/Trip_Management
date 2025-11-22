from models.attendance_model import AttendanceModel
from models.geofence_model import GeofenceModel
from models.upload_model import UploadModel
from geopy.distance import geodesic


class StudentController:

    # ---------------------------------------------------------
    # MARK ATTENDANCE (Option A — expects dict data)
    # ---------------------------------------------------------
    @staticmethod
    def mark_attendance(data):

        # 1️⃣ Required fields
        user_id = data.get("user_id")
        marked_lat = data.get("marked_lat")
        marked_lng = data.get("marked_lng")

        if not user_id:
            return {"success": False, "message": "User ID missing!"}

        if marked_lat is None or marked_lng is None:
            return {"success": False, "message": "GPS location missing!"}

        try:
            user_lat = float(marked_lat)
            user_lng = float(marked_lng)
        except:
            return {"success": False, "message": "Invalid GPS values!"}

        # 2️⃣ Load active geofence
        geofence = GeofenceModel.get_active_geofence()
        if not geofence:
            return {"success": False, "message": "No active geofence set by master!"}

        fence_lat = float(geofence["latitude"])
        fence_lng = float(geofence["longitude"])
        radius = float(geofence["radius"])

        # 3️⃣ Distance check
        distance = geodesic((fence_lat, fence_lng), (user_lat, user_lng)).meters

        if distance > radius:
            return {
                "success": False,
                "message": f"You are outside the geofence zone! Distance: {int(distance)}m"
            }

        # 4️⃣ Mark Attendance
        AttendanceModel.mark_attendance({
            "user_id": user_id,
            "geofence_id": geofence["id"],
            "status": "present",
            "marked_lat": user_lat,
            "marked_lng": user_lng,
            "distance": distance
        })

        return {"success": True, "message": "Attendance marked successfully!"}

    # ---------------------------------------------------------
    # UPLOAD PHOTO
    # ---------------------------------------------------------
    @staticmethod
    def upload_photo(data):
        UploadModel.save_upload(data)
        return {"success": True, "message": "Photo uploaded"}

    # ---------------------------------------------------------
    # MY ATTENDANCE HISTORY
    # ---------------------------------------------------------
    @staticmethod
    def my_attendance(user_id):
        records = AttendanceModel.get_user_attendance(user_id)
        return {"success": True, "data": records}
