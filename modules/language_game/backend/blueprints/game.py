import random
from datetime import datetime
from flask import Blueprint, request, jsonify
from ..models import db, Question, LearningRecord, Employee, WrongQuestion, Badge, EmployeeBadge, LanguageReport
from ..utils import token_required

game_bp = Blueprint('game', __name__)

@game_bp.route('/questions/<int:lesson_id>', methods=['GET'])
@token_required
def get_questions(lesson_id):
    mode = request.args.get('mode', 'practice') # 'practice' or 'boss'
    
    questions = Question.query.filter_by(lesson_id=lesson_id).all()
    if not questions:
        return jsonify({'message': 'No questions found for this lesson'}), 404
        
    # If Boss battle, select exactly 20 random questions.
    # If practice, select 10 random questions.
    sample_size = 20 if mode == 'boss' else 10
    selected = random.sample(questions, min(sample_size, len(questions)))
    
    return jsonify([q.to_dict() for q in selected]), 200

@game_bp.route('/game/submit', methods=['POST'])
@token_required
def submit_game():
    employee_id = request.employee_id
    data = request.get_json() or {}
    
    lesson_id = data.get('lesson_id')
    correct_count = data.get('correct_count', 0)
    total_count = data.get('total_count', 10)
    time_spent = data.get('time_spent', 0) # in seconds
    max_combo = data.get('max_combo', 0)
    mode = data.get('mode', 'practice')
    
    # Calculate score & pass rate
    accuracy = correct_count / total_count if total_count > 0 else 0
    pass_rate = accuracy * 100
    
    # Calculate XP
    # +10 XP for each correct answer
    # Combo bonus: max_combo * 2 XP
    xp_gained = (correct_count * 10) + (max_combo * 2)
    
    employee = Employee.query.get(employee_id)
    if not employee:
        return jsonify({'message': 'Employee not found'}), 404
        
    # Save Learning Record
    record = LearningRecord(
        employee_id=employee_id,
        lesson_id=lesson_id,
        study_time=time_spent,
        pass_rate=pass_rate,
        accuracy=accuracy,
        max_combo=max_combo,
        xp_gained=xp_gained,
        study_date=datetime.utcnow().date()
    )
    db.session.add(record)
    
    # Update employee total XP and level
    employee.xp += xp_gained
    # LV100 max, 100 XP per level
    new_level = min(100, 1 + (employee.xp // 100))
    level_up = new_level > employee.level
    employee.level = new_level
    
    # Process wrong questions logged during the practice
    wrong_question_ids = data.get('wrong_question_ids', [])
    for q_id in wrong_question_ids:
        wq = WrongQuestion.query.filter_by(employee_id=employee_id, question_id=q_id).first()
        if wq:
            wq.wrong_count += 1
        else:
            wq = WrongQuestion(employee_id=employee_id, question_id=q_id, wrong_count=1)
            db.session.add(wq)
            
    # Process correct questions that were in the wrong question list (clear them or reduce count)
    correct_question_ids = data.get('correct_question_ids', [])
    for q_id in correct_question_ids:
        wq = WrongQuestion.query.filter_by(employee_id=employee_id, question_id=q_id).first()
        if wq:
            db.session.delete(wq)
            
    # Update capability report metrics
    report = LanguageReport.query.filter_by(employee_id=employee_id).first()
    if not report:
        report = LanguageReport(employee_id=employee_id)
        db.session.add(report)
        
    # Standard values increment based on lesson focus
    # E.g. lessons 1-8 are vocab, 9 is grammar, 10-14 dialogue/vocab, 15-21 safety/work
    if lesson_id <= 8:
        report.score_vocabulary = min(100.0, report.score_vocabulary + (accuracy * 5.0))
    elif lesson_id == 9:
        report.score_grammar = min(100.0, report.score_grammar + (accuracy * 10.0))
    elif lesson_id in [10, 11, 12, 13, 14]:
        report.score_vocabulary = min(100.0, report.score_vocabulary + (accuracy * 3.0))
        report.score_dialogue = min(100.0, report.score_dialogue + (accuracy * 6.0))
    elif lesson_id in [15, 16, 17]:
        report.score_work = min(100.0, report.score_work + (accuracy * 5.0))
        report.score_dialogue = min(100.0, report.score_dialogue + (accuracy * 3.0))
    else: # 18, 19, 20, 21
        report.score_safety = min(100.0, report.score_safety + (accuracy * 8.0))
        report.score_work = min(100.0, report.score_work + (accuracy * 4.0))
        
    # Recalculate level (A1-C2) based on average metrics
    avg_score = (report.score_vocabulary + report.score_grammar + report.score_dialogue + report.score_safety + report.score_work) / 5.0
    if avg_score >= 90:
        report.level = 'C2'
    elif avg_score >= 80:
        report.level = 'C1'
    elif avg_score >= 65:
        report.level = 'B2'
    elif avg_score >= 50:
        report.level = 'B1'
    elif avg_score >= 30:
        report.level = 'A2'
    else:
        report.level = 'A1'
        
    # Check and award badges
    new_badges = []
    
    # 1. First Pass Badge
    first_pass_badge = Badge.query.filter_by(trigger_type='first_pass').first()
    if first_pass_badge:
        eb = EmployeeBadge.query.filter_by(employee_id=employee_id, badge_id=first_pass_badge.id).first()
        if not eb and pass_rate >= 80:
            eb = EmployeeBadge(employee_id=employee_id, badge_id=first_pass_badge.id)
            db.session.add(eb)
            new_badges.append(first_pass_badge.to_dict())
            
    # 2. Vocabulary Master (e.g. Vocab score >= 50)
    vocab_badge = Badge.query.filter_by(trigger_type='vocab_master').first()
    if vocab_badge:
        eb = EmployeeBadge.query.filter_by(employee_id=employee_id, badge_id=vocab_badge.id).first()
        if not eb and report.score_vocabulary >= 50.0:
            eb = EmployeeBadge(employee_id=employee_id, badge_id=vocab_badge.id)
            db.session.add(eb)
            new_badges.append(vocab_badge.to_dict())

    # 3. Safety Master (e.g. Safety score >= 50)
    safety_badge = Badge.query.filter_by(trigger_type='safety_master').first()
    if safety_badge:
        eb = EmployeeBadge.query.filter_by(employee_id=employee_id, badge_id=safety_badge.id).first()
        if not eb and report.score_safety >= 50.0:
            eb = EmployeeBadge(employee_id=employee_id, badge_id=safety_badge.id)
            db.session.add(eb)
            new_badges.append(safety_badge.to_dict())

    # 4. Work Master (e.g. Work score >= 50)
    work_badge = Badge.query.filter_by(trigger_type='work_master').first()
    if work_badge:
        eb = EmployeeBadge.query.filter_by(employee_id=employee_id, badge_id=work_badge.id).first()
        if not eb and report.score_work >= 50.0:
            eb = EmployeeBadge(employee_id=employee_id, badge_id=work_badge.id)
            db.session.add(eb)
            new_badges.append(work_badge.to_dict())

    db.session.commit()
    
    return jsonify({
        'message': 'Results submitted successfully',
        'xp_gained': xp_gained,
        'level_up': level_up,
        'new_level': employee.level,
        'passed': pass_rate >= 80,
        'new_badges': new_badges
    }), 200

@game_bp.route('/wrong-questions', methods=['GET'])
@token_required
def get_wrong_questions():
    employee_id = request.employee_id
    wqs = WrongQuestion.query.filter_by(employee_id=employee_id).all()
    return jsonify([wq.to_dict() for wq in wqs if wq.question is not None]), 200

@game_bp.route('/wrong-questions/submit', methods=['POST'])
@token_required
def add_wrong_question():
    employee_id = request.employee_id
    data = request.get_json() or {}
    q_id = data.get('question_id')
    
    if not q_id:
        return jsonify({'message': 'Missing question_id'}), 400
        
    wq = WrongQuestion.query.filter_by(employee_id=employee_id, question_id=q_id).first()
    if wq:
        wq.wrong_count += 1
    else:
        wq = WrongQuestion(employee_id=employee_id, question_id=q_id, wrong_count=1)
        db.session.add(wq)
        
    db.session.commit()
    return jsonify({'message': 'Logged wrong question'}), 200

@game_bp.route('/wrong-questions/remove', methods=['POST'])
@token_required
def remove_wrong_question():
    employee_id = request.employee_id
    data = request.get_json() or {}
    q_id = data.get('question_id')
    
    if not q_id:
        return jsonify({'message': 'Missing question_id'}), 400
        
    wq = WrongQuestion.query.filter_by(employee_id=employee_id, question_id=q_id).first()
    if wq:
        db.session.delete(wq)
        db.session.commit()
        
    return jsonify({'message': 'Removed wrong question'}), 200
