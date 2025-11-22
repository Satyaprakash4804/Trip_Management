import secrets

class TokenHelper:

    @staticmethod
    def generate_token():
        return secrets.token_hex(32)

    @staticmethod
    def validate_token(token, stored_token):
        return token == stored_token
