import jwt

from flask import request

from functools import wraps

from instance.config import secret_key

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'X-API-KEY' in request.headers:
            token = request.headers['X-API-KEY']
        if not token:
            return {'result': 'No token found'}, 401

        try:
            token = jwt.decode(token, 'notsosecret', algorithms='HS256'), 401
        except:
            return {'result': 'Invalid token'}, 401
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    @wraps(f)
    def endpoint_decorate(*args, **kwargs):
        token = None
        if 'X-API-KEY' in request.headers:
            token = request.headers['X-API-KEY']
        if not token:
            return {'result': 'No token found'}, 401

        try:
            token = jwt.decode(token, secret_key, algorithms='HS256'), 401
        except:
            return {'result': 'Invalid token'}, 401
        return f(*args, **kwargs)
    return endpoint_decorate