import jwt
import datetime
from werkzeug.exceptions import Unauthorized
from config import Config


class JwtError(Exception):
    """Exception raised for jwt errors in the quiz app 
    """

    def __init__(self, message="Jwt error"):
        self.message = message
        super().__init__(self.message)


secret = Config.SECRET_KEY
expiration_in_seconds = Config.EXPIRATION_IN_SECONDS

def build_token():
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=expiration_in_seconds),
            'iat': datetime.datetime.utcnow(),
            'sub': 'quiz-app-admin'
        }
        return {
            "token": jwt.encode(payload, secret, algorithm="HS256"),
            "expiration": expiration_in_seconds
		}
    except Exception as e:
        return e


def decode_token(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(auth_token, secret, algorithms="HS256")
        # if decoding did not fail, this means we are correctly logged in
        return payload['sub']
    except jwt.ExpiredSignatureError:
        raise JwtError('Signature expired. Please log in again.')
    except jwt.InvalidTokenError as e:
        raise JwtError('Invalid token. Please log in again.')

def auth_midleware(request):
    token = request.headers.get('Authorization')
    
    if not token:
        raise Unauthorized("Token is missing")
    
    # Cut Bearer from token
    token = token.split(" ")[1]
    
    try:
        decode_token(token)
    except JwtError as e:
        raise Unauthorized(str(e))
    return True