import os
import jwt
from flask import jsonify, request
from functools import wraps
import datetime



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

def generate_token_jwt(username):
    try:
        token = jwt.encode({
                'user' : username,
                'exp'  : datetime.datetime.utcnow() + datetime.timedelta(seconds=60)
            },
            secret)
        return token
    except Exception as e:
        print("----------------%s---------" %e)