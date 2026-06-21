import os
import jwt
import datetime
from functools import wraps
from flask import request, jsonify, current_app

SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'iwip_indonesia_secret_key_998877')

def generate_token(employee_id, role):
    payload = {
        'sub': employee_id,
        'role': role,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
        'iat': datetime.datetime.utcnow()
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return 'Token expired'
    except jwt.InvalidTokenError:
        return 'Invalid token'

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({'message': 'Authorization token is missing'}), 401
        
        data = verify_token(token)
        if isinstance(data, str):
            return jsonify({'message': f'Unauthorized: {data}'}), 401
            
        # Add employee_id and role to request context
        request.employee_id = data['sub']
        request.employee_role = data['role']
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({'message': 'Authorization token is missing'}), 401
        
        data = verify_token(token)
        if isinstance(data, str) or data['role'] != 'admin':
            return jsonify({'message': 'Admin privileges required'}), 403
            
        request.employee_id = data['sub']
        request.employee_role = data['role']
        return f(*args, **kwargs)
    return decorated
