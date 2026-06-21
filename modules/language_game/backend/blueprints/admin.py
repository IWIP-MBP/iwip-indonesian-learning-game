import csv
import io
from flask import Blueprint, request, jsonify, send_file
from ..models import db, Employee, Department, LearningRecord, LanguageReport
from ..utils import admin_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/employees', methods=['GET'])
@admin_required
def get_employees():
    employees = Employee.query.all()
    return jsonify([emp.to_dict() for emp in employees]), 200

@admin_bp.route('/admin/departments', methods=['GET'])
@admin_required
def get_departments():
    departments = Department.query.all()
    return jsonify([dept.to_dict() for dept in departments]), 200

@admin_bp.route('/admin/employees', methods=['POST'])
@admin_required
def create_employee():
    data = request.get_json() or {}
    emp_id = data.get('id')
    name = data.get('name')
    dept_id = data.get('department_id')
    password = data.get('password')
    role = data.get('role', 'employee')
    
    if not emp_id or not name or not password:
        return jsonify({'message': '工号、姓名和密码为必填项'}), 400
        
    existing = Employee.query.get(emp_id)
    if existing:
        return jsonify({'message': '该工号已存在'}), 400
        
    employee = Employee(id=emp_id, name=name, department_id=dept_id, role=role)
    employee.set_password(password)
    db.session.add(employee)
    
    # Initialize report card
    report = LanguageReport(employee_id=emp_id)
    db.session.add(report)
    
    db.session.commit()
    return jsonify(employee.to_dict()), 201

@admin_bp.route('/admin/employees/<string:emp_id>', methods=['PUT'])
@admin_required
def update_employee(emp_id):
    employee = Employee.query.get(emp_id)
    if not employee:
        return jsonify({'message': '员工未找到'}), 404
        
    data = request.get_json() or {}
    employee.name = data.get('name', employee.name)
    employee.department_id = data.get('department_id', employee.department_id)
    employee.role = data.get('role', employee.role)
    
    password = data.get('password')
    if password:
        employee.set_password(password)
        
    db.session.commit()
    return jsonify(employee.to_dict()), 200

@admin_bp.route('/admin/employees/<string:emp_id>', methods=['DELETE'])
@admin_required
def delete_employee(emp_id):
    employee = Employee.query.get(emp_id)
    if not employee:
        return jsonify({'message': '员工未找到'}), 404
        
    db.session.delete(employee)
    db.session.commit()
    return jsonify({'message': '员工已删除'}), 200

@admin_bp.route('/admin/employees/import-json', methods=['POST'])
@admin_required
def import_employees_json():
    # JSON import: [{"id":"E001", "name":"张三", "department":"后勤部", "password":"123"}]
    data = request.get_json() or []
    imported_count = 0
    errors = []
    
    for item in data:
        emp_id = item.get('id') or item.get('工号')
        name = item.get('name') or item.get('姓名')
        dept_name = item.get('department') or item.get('部门')
        password = str(item.get('password') or item.get('密码') or '123456')
        
        if not emp_id or not name:
            errors.append(f"数据行缺少必填项：{item}")
            continue
            
        existing = Employee.query.get(emp_id)
        if existing:
            errors.append(f"工号 {emp_id} 已存在，跳过该条数据。")
            continue
            
        # Find or create department
        dept_id = None
        if dept_name:
            dept = Department.query.filter_by(name=dept_name).first()
            if not dept:
                dept = Department(name=dept_name)
                db.session.add(dept)
                db.session.commit()
            dept_id = dept.id
            
        employee = Employee(id=emp_id, name=name, department_id=dept_id, role='employee')
        employee.set_password(password)
        db.session.add(employee)
        
        # Initialize report card
        report = LanguageReport(employee_id=emp_id)
        db.session.add(report)
        
        imported_count += 1
        
    db.session.commit()
    return jsonify({
        'message': f'成功导入 {imported_count} 名员工',
        'errors': errors
    }), 200

@admin_bp.route('/admin/reports/export', methods=['GET'])
@admin_required
def export_reports_csv():
    # Fetch learning statistics for all employees
    employees = Employee.query.all()
    
    # Generate CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Headers
    writer.writerow([
        '工号', '姓名', '部门', '总XP', '游戏等级', 
        '印尼语能力评级', '词汇得分', '语法得分', '对话得分', '安全场景得分', '办公场景得分'
    ])
    
    for emp in employees:
        rep = LanguageReport.query.filter_by(employee_id=emp.id).first()
        writer.writerow([
            emp.id,
            emp.name,
            emp.department.name if emp.department else '无部门',
            emp.xp,
            emp.level,
            rep.level if rep else 'A1',
            round(rep.score_vocabulary, 1) if rep else 0.0,
            round(rep.score_grammar, 1) if rep else 0.0,
            round(rep.score_dialogue, 1) if rep else 0.0,
            round(rep.score_safety, 1) if rep else 0.0,
            round(rep.score_work, 1) if rep else 0.0
        ])
        
    # Return file stream
    output.seek(0)
    # Ensure correct encoding (utf-8-sig for Excel compatibility)
    mem_file = io.BytesIO(output.getvalue().encode('utf-8-sig'))
    
    return send_file(
        mem_file,
        mimetype='text/csv',
        as_attachment=True,
        download_name='employees_learning_report.csv'
    )
