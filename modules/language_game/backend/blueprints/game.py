import random, math
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
from ..models import db, Question, LearningRecord, Employee, WrongQuestion, Badge, EmployeeBadge, LanguageReport
from ..utils import token_required

game_bp = Blueprint("game", __name__)

print("module loaded ok")

# Difficulty configuration
DIFFICULTY_MAP = {
    "vocab_choice": 1, "indo_to_cn": 1, "picture": 1,
    "cn_to_indo": 2, "audio": 2, "drag_match": 2,
    "fill_blank": 2, "word_sort": 3, "dialogue": 3,
}

# Lesson-type vs question-type weight config
LESSON_WEIGHTS = {
    "pronunciation": {
        "vocab_choice": 3, "indo_to_cn": 3, "cn_to_indo": 2,
        "audio": 5, "picture": 2, "fill_blank": 1,
        "word_sort": 0, "dialogue": 0, "drag_match": 1,
    },
    "regular": {
        "vocab_choice": 3, "indo_to_cn": 3, "cn_to_indo": 3,
        "audio": 2, "picture": 1, "fill_blank": 3,
        "word_sort": 2, "dialogue": 3, "drag_match": 2,
    },
    "grammar": {
        "vocab_choice": 1, "indo_to_cn": 1, "cn_to_indo": 2,
        "audio": 1, "picture": 0, "fill_blank": 4,
        "word_sort": 3, "dialogue": 2, "drag_match": 3,
    },
    "safety": {
        "vocab_choice": 2, "indo_to_cn": 2, "cn_to_indo": 2,
        "audio": 2, "picture": 2, "fill_blank": 3,
        "word_sort": 2, "dialogue": 4, "drag_match": 3,
    },
}

def get_lesson_category(lesson_id):
    if lesson_id <= 8:
        return "pronunciation"
    elif lesson_id == 9:
        return "grammar"
    elif lesson_id >= 15:
        return "safety"
    return "regular"


def get_diff_key(q):
    return DIFFICULTY_MAP.get(q.type, 2)


def weighted_sample(questions, weights, count):
    if not questions or count <= 0:
        return []

    type_groups = {}
    for q in questions:
        type_groups.setdefault(q.type, []).append(q)

    total_weight = sum(weights.get(qt, 1) for qt in type_groups if type_groups[qt])
    if total_weight == 0:
        return random.sample(questions, min(count, len(questions)))

    raw_quotas = {}
    remaining = count
    for qt, weight in weights.items():
        if weight > 0 and qt in type_groups and type_groups[qt]:
            qty = count * weight // total_weight
            raw_quotas[qt] = qty
            remaining -= qty

    sorted_types = sorted(
        [(qt, weights.get(qt, 1)) for qt in type_groups],
        key=lambda x: -x[1],
    )
    for qt, _ in sorted_types:
        if remaining <= 0:
            break
        if qt in raw_quotas:
            extra = min(remaining, len(type_groups[qt]) - raw_quotas[qt])
            raw_quotas[qt] += extra
            remaining -= extra

    result = []
    used_ids = set()

    for qt, quota in raw_quotas.items():
        if quota <= 0:
            continue
        pool = [q for q in type_groups.get(qt, []) if q.id not in used_ids]
        if not pool:
            continue
        sample_size = min(quota, len(pool))
        chosen = random.sample(pool, sample_size)
        result.extend(chosen)
        used_ids.update(q.id for q in chosen)

    random.shuffle(result)

    if len(result) < count:
        remaining_pool = [q for q in questions if q.id not in used_ids]
        extras = random.sample(
            remaining_pool, min(count - len(result), len(remaining_pool))
        )
        result.extend(extras)

    return result


@game_bp.route("/questions/<int:lesson_id>", methods=["GET"])
@token_required
def get_questions(lesson_id):
    mode = request.args.get("mode", "practice")

    questions = Question.query.filter_by(lesson_id=lesson_id).all()
    if not questions:
        return jsonify({"message": "No questions found for this lesson"}), 404

    lesson_type = get_lesson_category(lesson_id)
    weights = LESSON_WEIGHTS.get(lesson_type, LESSON_WEIGHTS["regular"])

    total_needed = 20 if mode == "boss" else 10
    selected = weighted_sample(questions, weights, total_needed)
    selected.sort(key=lambda q: (get_diff_key(q), random.random()))

    return jsonify([q.to_dict() for q in selected]), 200


@game_bp.route("/game/submit", methods=["POST"])
@token_required
def submit_game():
    employee_id = request.employee_id
    data = request.get_json() or {}

    lesson_id = data.get("lesson_id")
    correct_count = data.get("correct_count", 0)
    total_count = data.get("total_count", 10)
    time_spent = data.get("time_spent", 0)
    max_combo = data.get("max_combo", 0)
    mode = data.get("mode", "practice")

    accuracy = correct_count / total_count if total_count > 0 else 0
    pass_rate = accuracy * 100

    xp_base = (correct_count * 10) + (max_combo * 2)
    if mode == "boss":
        xp_base = int(xp_base * 1.5)
    xp_gained = xp_base

    employee = Employee.query.get(employee_id)
    if not employee:
        return jsonify({"message": "Employee not found"}), 404

    record = LearningRecord(
        employee_id=employee_id,
        lesson_id=lesson_id,
        study_time=time_spent,
        pass_rate=pass_rate,
        accuracy=accuracy,
        max_combo=max_combo,
        xp_gained=xp_gained,
        study_date=datetime.utcnow().date(),
    )
    db.session.add(record)

    employee.xp += xp_gained
    new_level = min(100, 1 + (employee.xp // 100))
    level_up = new_level > employee.level
    employee.level = new_level

    # Spaced Repetition: wrong questions
    wrong_question_ids = data.get("wrong_question_ids", [])
    for q_id in wrong_question_ids:
        wq = WrongQuestion.query.filter_by(
            employee_id=employee_id, question_id=q_id
        ).first()
        now = datetime.utcnow()
        if wq:
            wq.wrong_count += 1
            wq.last_wrong_at = now
            wq.recall_count = 0
        else:
            wq = WrongQuestion(
                employee_id=employee_id,
                question_id=q_id,
                wrong_count=1,
                last_wrong_at=now,
                recall_count=0,
            )
            db.session.add(wq)

    # Spaced Repetition: correct answers from wrong list
    correct_question_ids = data.get("correct_question_ids", [])
    for q_id in correct_question_ids:
        wq = WrongQuestion.query.filter_by(
            employee_id=employee_id, question_id=q_id
        ).first()
        if wq:
            wq.recall_count = (wq.recall_count or 0) + 1
            if wq.recall_count >= 2:
                db.session.delete(wq)
            else:
                wq.last_wrong_at = datetime.utcnow()

    # Update capability report
    report = LanguageReport.query.filter_by(employee_id=employee_id).first()
    if not report:
        report = LanguageReport(employee_id=employee_id)
        db.session.add(report)

    lesson_category = get_lesson_category(lesson_id)
    lr = 0.15

    # Protect against None values from DB
    report.score_vocabulary = report.score_vocabulary or 0.0
    report.score_grammar = report.score_grammar or 0.0
    report.score_dialogue = report.score_dialogue or 0.0
    report.score_safety = report.score_safety or 0.0
    report.score_work = report.score_work or 0.0

    if lesson_category == "pronunciation":
        report.score_vocabulary = (
            report.score_vocabulary * (1 - lr) + (accuracy * 100 * lr)
        )
    elif lesson_category == "grammar":
        report.score_grammar = report.score_grammar * (1 - lr) + (
            accuracy * 100 * lr
        )
    elif lesson_category == "safety":
        report.score_safety = report.score_safety * (1 - lr * 0.6) + (
            accuracy * 100 * lr * 0.6
        )
        report.score_work = report.score_work * (1 - lr * 0.4) + (
            accuracy * 100 * lr * 0.4
        )
        report.score_dialogue = report.score_dialogue * (1 - lr * 0.2) + (
            accuracy * 100 * lr * 0.2
        )
    else:
        report.score_vocabulary = report.score_vocabulary * (
            1 - lr * 0.4
        ) + (accuracy * 100 * lr * 0.4)
        report.score_dialogue = report.score_dialogue * (1 - lr * 0.6) + (
            accuracy * 100 * lr * 0.6
        )

    avg_score = (
        report.score_vocabulary
        + report.score_grammar
        + report.score_dialogue
        + report.score_safety
        + report.score_work
    ) / 5.0

    if avg_score >= 90:
        report.level = "C2"
    elif avg_score >= 80:
        report.level = "C1"
    elif avg_score >= 65:
        report.level = "B2"
    elif avg_score >= 50:
        report.level = "B1"
    elif avg_score >= 30:
        report.level = "A2"
    else:
        report.level = "A1"

    new_badges = []

    first_pass_badge = Badge.query.filter_by(trigger_type="first_pass").first()
    if first_pass_badge:
        eb = EmployeeBadge.query.filter_by(
            employee_id=employee_id, badge_id=first_pass_badge.id
        ).first()
        if not eb and pass_rate >= 80:
            eb = EmployeeBadge(
                employee_id=employee_id, badge_id=first_pass_badge.id
            )
            db.session.add(eb)
            new_badges.append(first_pass_badge.to_dict())

    vocab_badge = Badge.query.filter_by(trigger_type="vocab_master").first()
    if vocab_badge:
        eb = EmployeeBadge.query.filter_by(
            employee_id=employee_id, badge_id=vocab_badge.id
        ).first()
        if not eb and report.score_vocabulary >= 50.0:
            eb = EmployeeBadge(
                employee_id=employee_id, badge_id=vocab_badge.id
            )
            db.session.add(eb)
            new_badges.append(vocab_badge.to_dict())

    safety_badge = Badge.query.filter_by(trigger_type="safety_master").first()
    if safety_badge:
        eb = EmployeeBadge.query.filter_by(
            employee_id=employee_id, badge_id=safety_badge.id
        ).first()
        if not eb and report.score_safety >= 50.0:
            eb = EmployeeBadge(
                employee_id=employee_id, badge_id=safety_badge.id
            )
            db.session.add(eb)
            new_badges.append(safety_badge.to_dict())

    work_badge = Badge.query.filter_by(trigger_type="work_master").first()
    if work_badge:
        eb = EmployeeBadge.query.filter_by(
            employee_id=employee_id, badge_id=work_badge.id
        ).first()
        if not eb and report.score_work >= 50.0:
            eb = EmployeeBadge(
                employee_id=employee_id, badge_id=work_badge.id
            )
            db.session.add(eb)
            new_badges.append(work_badge.to_dict())

    db.session.commit()

    return jsonify(
        {
            "message": "Results submitted successfully",
            "xp_gained": xp_gained,
            "level_up": level_up,
            "new_level": employee.level,
            "passed": pass_rate >= 80,
            "new_badges": new_badges,
        }
    ), 200


@game_bp.route("/wrong-questions", methods=["GET"])
@token_required
def get_wrong_questions():
    employee_id = request.employee_id
    today = datetime.utcnow().date()

    wqs = WrongQuestion.query.filter_by(employee_id=employee_id).all()

    scored = []
    for wq in wqs:
        if wq.question is None:
            continue
        last_wrong = wq.last_wrong_at.date() if wq.last_wrong_at else today
        days_since = (today - last_wrong).days
        priority = (wq.wrong_count or 0) * 3 + min(days_since, 30) - (
            wq.recall_count or 0
        ) * 5
        scored.append((priority, wq))

    scored.sort(key=lambda x: -x[0])
    return jsonify([wq.to_dict() for _, wq in scored]), 200


@game_bp.route("/wrong-questions/submit", methods=["POST"])
@token_required
def add_wrong_question():
    employee_id = request.employee_id
    data = request.get_json() or {}
    q_id = data.get("question_id")

    if not q_id:
        return jsonify({"message": "Missing question_id"}), 400

    wq = WrongQuestion.query.filter_by(
        employee_id=employee_id, question_id=q_id
    ).first()
    if wq:
        wq.wrong_count += 1
        wq.last_wrong_at = datetime.utcnow()
        wq.recall_count = 0
    else:
        wq = WrongQuestion(
            employee_id=employee_id,
            question_id=q_id,
            wrong_count=1,
            last_wrong_at=datetime.utcnow(),
            recall_count=0,
        )
        db.session.add(wq)

    db.session.commit()
    return jsonify({"message": "Logged wrong question"}), 200


@game_bp.route("/wrong-questions/remove", methods=["POST"])
@token_required
def remove_wrong_question():
    employee_id = request.employee_id
    data = request.get_json() or {}
    q_id = data.get("question_id")

    if not q_id:
        return jsonify({"message": "Missing question_id"}), 400

    wq = WrongQuestion.query.filter_by(
        employee_id=employee_id, question_id=q_id
    ).first()
    if wq:
        db.session.delete(wq)
        db.session.commit()

    return jsonify({"message": "Removed wrong question"}), 200


@game_bp.route("/wrong-questions/review", methods=["GET"])
@token_required
def get_wrong_questions_review():
    employee_id = request.employee_id
    today = datetime.utcnow().date()

    wqs = WrongQuestion.query.filter_by(employee_id=employee_id).all()

    scored = []
    for wq in wqs:
        if wq.question is None:
            continue
        last_wrong = wq.last_wrong_at.date() if wq.last_wrong_at else today
        days_since = (today - last_wrong).days
        priority = (wq.wrong_count or 0) * 3 + min(days_since, 30) - (
            wq.recall_count or 0
        ) * 5
        scored.append((priority, wq))

    scored.sort(key=lambda x: -x[0])

    result = []
    for _, wq in scored[:10]:
        q = wq.question
        if q:
            q_dict = q.to_dict()
            q_dict["wrong_count"] = wq.wrong_count
            q_dict["recall_count"] = wq.recall_count
            result.append(q_dict)

    return jsonify(result), 200
