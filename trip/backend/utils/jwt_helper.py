import jwt
import datetime
from config import Config

class JWTHelper:

    @staticmethod
    def create_token(user_data):
        SECRET = Config.JWT_SECRET_KEY

        if not isinstance(SECRET, str):
            raise TypeError("JWT_SECRET_KEY must be a string")

        payload = {
            "user": user_data,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(
                minutes=Config.JWT_EXP_MINUTES
            )
        }

        token = jwt.encode(payload, SECRET, algorithm="HS256")

        if isinstance(token, bytes):
            token = token.decode("utf-8")

        return token

    @staticmethod
    def verify_token(token):
        SECRET = Config.JWT_SECRET_KEY

        try:
            decoded = jwt.decode(token, SECRET, algorithms=["HS256"])
            return decoded["user"], True
        except Exception:
            return None, False
