from flask import Blueprint, request, jsonify
from ..models import db, Employee, Department
from ..utils import generate_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    employee_id = data.get('employee_id') or data.get('id')
    password = data.get('password')
    
    if not employee_id or not password:
        return jsonify({'message': '请输入工号和密码'}), 400
        
    employee = Employee.query.get(employee_id)
    if not employee or not employee.check_password(password):
        return jsonify({'message': '工号或密码不正确'}), 401
        
    token = generate_token(employee.id, employee.role)
    
    return jsonify({
        'id': employee.id,
        'name': employee.name,
        'department': employee.department.name if employee.department else '无部门',
        'role': employee.role,
        'token': token
    }), 200
