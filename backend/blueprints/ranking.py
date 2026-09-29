from flask import Blueprint, request, jsonify
from sqlalchemy import func
from ..models import db, Employee, Department
from ..utils import token_required

ranking_bp = Blueprint('ranking', __name__)

@ranking_bp.route('/rankings', methods=['GET'])
@token_required
def get_rankings():
    # 1. Company Rankings (Top 50 employees by XP)
    company_ranks = Employee.query.order_by(Employee.xp.desc()).limit(50).all()
    company_list = []
    for idx, emp in enumerate(company_ranks):
        company_list.append({
            'rank': idx + 1,
            'id': emp.id,
            'name': emp.name,
            'department': emp.department.name if emp.department else '无部门',
            'xp': emp.xp,
            'level': emp.level
        })
        
    # 2. Department Rankings (Sorted by average employee XP)
    dept_ranks = db.session.query(
        Department.name,
        func.avg(Employee.xp).label('avg_xp'),
        func.count(Employee.id).label('emp_count')
    ).join(Employee, Department.id == Employee.department_id)\
     .group_by(Department.id)\
     .order_by(func.avg(Employee.xp).desc()).all()
     
    dept_list = []
    for idx, r in enumerate(dept_ranks):
        dept_list.append({
            'rank': idx + 1,
            'department': r[0],
            'avg_xp': round(float(r[1]), 1) if r[1] is not None else 0.0,
            'emp_count': r[2]
        })
        
    # 3. Personal Rank context (Find current employee's exact rank in the company)
    current_employee_id = request.employee_id
    current_emp = Employee.query.get(current_employee_id)
    
    personal_rank = 0
    if current_emp:
        # Count how many employees have strictly higher XP
        higher_count = Employee.query.filter(Employee.xp > current_emp.xp).count()
        personal_rank = higher_count + 1
        
    return jsonify({
        'personal': {
            'rank': personal_rank,
            'xp': current_emp.xp if current_emp else 0,
            'level': current_emp.level if current_emp else 1
        },
        'company': company_list,
        'department': dept_list
    }), 200
