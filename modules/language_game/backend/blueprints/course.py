from flask import Blueprint, request, jsonify
from ..models import db, Lesson, LearningRecord, Vocabulary, Sentence, Dialogue, Grammar
from ..utils import token_required

course_bp = Blueprint('course', __name__)

@course_bp.route('/lessons', methods=['GET'])
@token_required
def get_lessons():
    employee_id = request.employee_id
    lessons = Lesson.query.order_by(Lesson.id).all()
    
    # Fetch passed lesson IDs for this employee
    # A lesson is passed if there's a record with accuracy >= 0.8 or general completions
    passed_lessons = db.session.query(LearningRecord.lesson_id).filter(
        LearningRecord.employee_id == employee_id
    ).distinct().all()
    passed_ids = {r[0] for r in passed_lessons}
    
    result = []
    for lesson in lessons:
        lesson_dict = lesson.to_dict()
        
        # Unlock logic:
        # Lesson 1 is always unlocked.
        # Lesson K is unlocked if Lesson K-1 is in passed_ids.
        if lesson.id == 1:
            unlocked = True
        else:
            unlocked = (lesson.id - 1) in passed_ids
            
        lesson_dict['unlocked'] = unlocked
        lesson_dict['completed'] = lesson.id in passed_ids
        result.append(lesson_dict)
        
    return jsonify(result), 200

@course_bp.route('/lessons/<int:lesson_id>', methods=['GET'])
@token_required
def get_lesson_detail(lesson_id):
    lesson = Lesson.query.get(lesson_id)
    if not lesson:
        return jsonify({'message': 'Lesson not found'}), 404
        
    # Check unlock status
    employee_id = request.employee_id
    if lesson_id > 1:
        prev_passed = LearningRecord.query.filter_by(
            employee_id=employee_id, lesson_id=lesson_id-1
        ).first()
        if not prev_passed:
            return jsonify({'message': 'This lesson is locked'}), 403
            
    vocab = [v.to_dict() for v in lesson.vocabulary]
    sents = [s.to_dict() for s in lesson.sentences]
    dials = [d.to_dict() for d in lesson.dialogues]
    gram = [g.to_dict() for g in lesson.grammar]
    
    return jsonify({
        'lesson': lesson.to_dict(),
        'vocabulary': vocab,
        'sentences': sents,
        'dialogues': dials,
        'grammar': gram
    }), 200
