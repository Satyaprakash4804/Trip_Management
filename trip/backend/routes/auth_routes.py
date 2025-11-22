from flask import Blueprint, request, jsonify
from controllers.auth_controller import AuthController
from utils.jwt_helper import JWTHelper
import base64
import os

auth_bp = Blueprint("auth_bp", __name__)


# ------------------------- LOGIN -------------------------
@auth_bp.post("/login")
def login():
    result = AuthController.login(request.json)

    if result.get("need_register"):
        return jsonify(result)

    if not result.get("success"):
        return jsonify(result)

    token = result["token"]

    resp = jsonify(result)
    resp.set_cookie(
        "access_token",
        token,
        httponly=True,
        max_age=86400,
        secure=False,
        samesite="Lax"
    )
    return resp


# ------------------------- LOGOUT -------------------------
@auth_bp.get("/logout")
def logout():
    resp = jsonify({"success": True, "message": "Logout successful"})
    resp.set_cookie("access_token", "", expires=0)
    return resp


# ------------------------- CHECK LOGIN -------------------------
@auth_bp.get("/check")
def check_login():
    token = request.cookies.get("access_token")
    if not token:
        return jsonify({"logged_in": False})

    user, valid = JWTHelper.verify_token(token)
    if not valid:
        return jsonify({"logged_in": False})

    return jsonify({"logged_in": True, "user": user})


# ------------------------- COMPLETE REGISTRATION -------------------------
@auth_bp.post("/register_complete")
def register_complete():
    data = request.form.to_dict()
    user_id = data.get("user_id")

    if not user_id:
        return jsonify({"success": False, "message": "User ID missing"})

    # Ensure upload folders exist
    os.makedirs("uploads/selfies", exist_ok=True)
    os.makedirs("uploads/college_id", exist_ok=True)
    os.makedirs("uploads/aadhar_student", exist_ok=True)
    os.makedirs("uploads/aadhar_parent", exist_ok=True)

    files = {}

    # -------------------------------------------------------
    # HANDLE COMPRESSED BASE64 SELFIE (JPEG)
    # -------------------------------------------------------
    selfie_base64 = data.get("selfie")

    if selfie_base64 and selfie_base64.startswith("data:image"):
        try:
            img_data = selfie_base64.split(",")[1]
            img_bytes = base64.b64decode(img_data)

            # Save as JPG
            selfie_path = f"uploads/selfies/selfie_{user_id}.jpg"
            with open(selfie_path, "wb") as f:
                f.write(img_bytes)

            files["selfie"] = selfie_path

        except Exception as e:
            return jsonify({"success": False, "message": f"Selfie decode error: {str(e)}"})

    else:
        # Fallback file upload
        f = request.files.get("selfie")
        if f:
            selfie_path = "uploads/selfies/" + f.filename
            f.save(selfie_path)
            files["selfie"] = selfie_path

    # -------------------------------------------------------
    # COLLEGE ID CARD
    # -------------------------------------------------------
    college_id = request.files.get("college_id_card")
    if college_id:
        cid_path = "uploads/college_id/" + college_id.filename
        college_id.save(cid_path)
        files["college_id_card"] = cid_path

    # -------------------------------------------------------
    # AADHAR (STUDENT)
    # -------------------------------------------------------
    a1 = request.files.get("aadhar_student")
    if a1:
        path = "uploads/aadhar_student/" + a1.filename
        a1.save(path)
        files["aadhar_student"] = path

    # -------------------------------------------------------
    # AADHAR (PARENT)
    # -------------------------------------------------------
    a2 = request.files.get("aadhar_parent")
    if a2:
        path = "uploads/aadhar_parent/" + a2.filename
        a2.save(path)
        files["aadhar_parent"] = path

    # --------------------- SAVE TO DATABASE ---------------------
    result = AuthController.complete_registration(user_id, data, files)
    return jsonify(result)
