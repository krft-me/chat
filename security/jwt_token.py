import os
import jwt
from flask import jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
from functools import wraps


secret = os.environ.get('SECRET_KEY', '123456789')

def check_for_token(func):
    
    @wraps(func)
    def wrapped(*args, **kwargs):

        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message':'Missing or empty token'}),403
        try:
            data = jwt.decode(token, secret,algorithms=['HS256'])
        except:
            return jsonify({'message':'Invalid token'}),403
        return func(*args,**kwargs)
    return wrapped