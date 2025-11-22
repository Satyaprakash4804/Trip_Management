from utils.jwt_helper import JWTHelper
from models.user_model import UserModel

class AuthController:

    @staticmethod
    def login(data):
        username = data.get("username")
        password = data.get("password")

        user = UserModel.get_user_by_username(username)

        if not user:
            return {"success": False, "message": "User not found"}

        if user["password"] != password:
            return {"success": False, "message": "Incorrect password"}

        role = user["role"]

        # SUPER ADMIN bypass registration
        if role == "super_admin":
            token = JWTHelper.create_token({
                "id": user["id"],
                "role": role,
                "name": user["name"]
            })
            return {
                "success": True,
                "user": {
                    "id": user["id"],
                    "role": role,
                    "name": user["name"]
                },
                "token": token
            }

        # MASTER bypass registration
        if role == "master":
            token = JWTHelper.create_token({
                "id": user["id"],
                "role": role,
                "name": user["name"]
            })
            return {
                "success": True,
                "user": {
                    "id": user["id"],
                    "role": role,
                    "name": user["name"]
                },
                "token": token
            }

        # Student & Admin must complete registration
        if role in ["student", "admin"] and user["is_verified"] == 0:
            return {
                "success": True,
                "need_register": True,
                "user_id": user["id"]
            }

        # Normal login after verification
        token = JWTHelper.create_token({
            "id": user["id"],
            "role": role,
            "name": user["name"]
        })

        return {
            "success": True,
            "user": {
                "id": user["id"],
                "role": role,
                "name": user["name"]
            },
            "token": token
        }


    @staticmethod
    def complete_registration(user_id, data, files):
        try:
            result = UserModel.update_registration(user_id, data, files)

            if result:
                return {
                    "success": True,
                    "message": "Registration completed successfully"
                }
            return {
                "success": False,
                "message": "Unable to complete registration"
            }

        except Exception as e:
            return {"success": False, "message": f"Error: {str(e)}"}
