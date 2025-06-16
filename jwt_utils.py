import os
import jwt
from datetime import datetime, timedelta
from flask import current_app

JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 3600

def create_jwt_token(identity):
    payload = {
        'identity': identity,
        'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
    }
    secret = current_app.config['JWT_SECRET']
    return jwt.encode(payload, secret, algorithm=JWT_ALGORITHM)

def decode_jwt_token(token):
    try:
        secret = current_app.config['JWT_SECRET']
        payload = jwt.decode(token, secret, algorithms=[JWT_ALGORITHM])
        return payload['identity']
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None
