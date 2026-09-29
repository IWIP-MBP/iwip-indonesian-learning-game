from flask import Blueprint, request, jsonify
from sqlalchemy import func
from datetime import datetime, timedelta
from ..models import db, LearningRecord, LanguageReport, Employee, Department
from ..utils import token_required

report_bp = Blueprint('report', __name__)

@report_bp.route('/reports', methods=['GET'])
@token_required
def get_reports_data():
    employee_id = request.employee_id
    
    # 1. Radar Chart Data (Capability Report)
    report = LanguageReport.query.filter_by(employee_id=employee_id).first()
    radar_data = {
        'vocabulary': round(report.score_vocabulary, 1) if report else 0.0,
        'grammar': round(report.score_grammar, 1) if report else 0.0,
        'dialogue': round(report.score_dialogue, 1) if report else 0.0,
        'safety': round(report.score_safety, 1) if report else 0.0,
        'work': round(report.score_work, 1) if report else 0.0,
        'level': report.level if report else 'A1'
    }
    
    # 2. Line Chart Data (Study trends: XP gained and duration per day for the last 14 days)
    today = datetime.utcnow().date()
    start_date = today - timedelta(days=13)
    
    records = db.session.query(
        LearningRecord.study_date,
        func.sum(LearningRecord.xp_gained).label('xp'),
        func.sum(LearningRecord.study_time).label('time')
    ).filter(
        LearningRecord.employee_id == employee_id,
        LearningRecord.study_date >= start_date
    ).group_by(LearningRecord.study_date).all()
    
    records_map = {r[0]: {'xp': r[1], 'time': r[2]} for r in records}
    
    trend_dates = []
    trend_xp = []
    trend_time = []
    
    for i in range(14):
        curr_date = start_date + timedelta(days=i)
        trend_dates.append(curr_date.strftime('%m-%d'))
        if curr_date in records_map:
            trend_xp.append(int(records_map[curr_date]['xp'] or 0))
            trend_time.append(round((records_map[curr_date]['time'] or 0) / 60, 1)) # to minutes
        else:
            trend_xp.append(0)
            trend_time.append(0.0)
            
    # 3. Bar Chart Data (Department average comparison)
    dept_averages = db.session.query(
        Department.name,
        func.avg(Employee.xp).label('avg_xp')
    ).join(Employee, Department.id == Employee.department_id)\
     .group_by(Department.id).all()
     
    dept_names = [d[0] for d in dept_averages]
    dept_scores = [round(float(d[1]), 1) if d[1] is not None else 0.0 for d in dept_averages]
    
    # 4. Heatmap Calendar Data (Learning record frequency for the current year)
    year_start = datetime(datetime.utcnow().year, 1, 1).date()
    
    heatmap_records = db.session.query(
        LearningRecord.study_date,
        func.count(LearningRecord.id).label('count')
    ).filter(
        LearningRecord.employee_id == employee_id,
        LearningRecord.study_date >= year_start
    ).group_by(LearningRecord.study_date).all()
    
    heatmap_data = []
    for hr in heatmap_records:
        heatmap_data.append([
            hr[0].isoformat(),
            int(hr[1] or 0)
        ])
        
    return jsonify({
        'radar': radar_data,
        'trend': {
            'dates': trend_dates,
            'xp': trend_xp,
            'time': trend_time
        },
        'departments': {
            'names': dept_names,
            'scores': dept_scores
        },
        'heatmap': heatmap_data
    }), 200
