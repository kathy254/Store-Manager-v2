import jwt
from flask import request, jsonify, make_response
from app.api.v2.models.user_models import Users
from functools import wraps
from instance.config import secret_key


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        authentication_header = request.headers.get('Authorization')
        if authentication_header:
            try:
                #get the role in token
                token = authentication_header.split(" ")[1]
                identity = Users.decode_auth_token(token)

                if identity == 'Invalid token. Please log in again.':
                    return make_response(jsonify({
                        'status': 'failed',
                        'message': 'Invalid token. Please log in again.'
                    }), 401)

            except Exception:
                return make_response(jsonify({
                    'status': 'failed',
                    'message': 'You are not authorized.'
                }),401)

            if token:
                if identity['role'] == 'attendant':
                    return make_response(jsonify({
                        'status': 'failed',
                        'message': 'You are not an administrator'
                    }), 401)
        return f(*args, **kwargs)
    return decorated

def token_required(k):
    @wraps(k)
    def decorate_token(*args, **kwargs):
        token = None
        authentication_header = request.headers.get('Authorization')
        if authentication_header:
            try:
                token = authentication_header.split(" ")[1]
                identity = Users.decode_auth_token(token)
                if identity == 'Invalid token. Please log in again.':
                    return make_response(jsonify({
                        'status': 'failed',
                        'message': 'Invalid token. Please log in again.'
                    }),401)

            except Exception:
                return make_response(jsonify({
                    'status': 'failed',
                    'message': 'You are not authorized'
                }), 401)
        return k(*args, **kwargs)
    return decorate_token       