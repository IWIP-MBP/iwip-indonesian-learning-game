import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Department(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    employees = db.relationship('Employee', backref='department', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }

class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id', ondelete='SET NULL'), nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='employee')
    xp = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)
    
    records = db.relationship('LearningRecord', backref='employee', lazy=True, cascade='all, delete-orphan')
    wrong_questions = db.relationship('WrongQuestion', backref='employee', lazy=True, cascade='all, delete-orphan')
    badges = db.relationship('EmployeeBadge', backref='employee', lazy=True, cascade='all, delete-orphan')
    report = db.relationship('LanguageReport', backref='employee', uselist=False, lazy=True, cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        # Allow checking plain text for default seeded admins if needed, but normally use werkzeug security
        if self.password_hash.startswith('pbkdf2:sha256') or self.password_hash.startswith('scrypt'):
            return check_password_hash(self.password_hash, password)
        return self.password_hash == password

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'department_id': self.department_id,
            'department_name': self.department.name if self.department else '无部门',
            'role': self.role,
            'xp': self.xp,
            'level': self.level
        }

class Lesson(db.Model):
    __tablename__ = 'lessons'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(50), nullable=False) # 'pronunciation' or 'regular'
    
    vocabulary = db.relationship('Vocabulary', backref='lesson', lazy=True, cascade='all, delete-orphan')
    sentences = db.relationship('Sentence', backref='lesson', lazy=True, cascade='all, delete-orphan')
    dialogues = db.relationship('Dialogue', backref='lesson', lazy=True, cascade='all, delete-orphan')
    grammar = db.relationship('Grammar', backref='lesson', lazy=True, cascade='all, delete-orphan')
    questions = db.relationship('Question', backref='lesson', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'type': self.type
        }

class Vocabulary(db.Model):
    __tablename__ = 'vocabulary'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id', ondelete='CASCADE'), nullable=False)
    word = db.Column(db.String(255), nullable=False)
    translation = db.Column(db.String(255), nullable=False)
    phonetic = db.Column(db.String(255), nullable=True)
    audio_path = db.Column(db.String(255), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'lesson_id': self.lesson_id,
            'word': self.word,
            'translation': self.translation,
            'phonetic': self.phonetic,
            'audio_path': self.audio_path
        }

class Sentence(db.Model):
    __tablename__ = 'sentences'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id', ondelete='CASCADE'), nullable=False)
    indonesian = db.Column(db.Text, nullable=False)
    chinese = db.Column(db.Text, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'lesson_id': self.lesson_id,
            'indonesian': self.indonesian,
            'chinese': self.chinese
        }

class Dialogue(db.Model):
    __tablename__ = 'dialogues'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id', ondelete='CASCADE'), nullable=False)
    dialogue_group = db.Column(db.Integer, nullable=False)
    speaker = db.Column(db.String(50), nullable=True)
    indonesian = db.Column(db.Text, nullable=False)
    chinese = db.Column(db.Text, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'lesson_id': self.lesson_id,
            'dialogue_group': self.dialogue_group,
            'speaker': self.speaker,
            'indonesian': self.indonesian,
            'chinese': self.chinese
        }

class Grammar(db.Model):
    __tablename__ = 'grammar'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'lesson_id': self.lesson_id,
            'title': self.title,
            'content': self.content
        }

class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id', ondelete='CASCADE'), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    explanation = db.Column(db.Text, nullable=True)
    audio_path = db.Column(db.String(255), nullable=True)
    image_path = db.Column(db.String(255), nullable=True)
    options = db.relationship('QuestionOption', backref='question', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'lesson_id': self.lesson_id,
            'type': self.type,
            'content': self.content,
            'explanation': self.explanation,
            'audio_path': self.audio_path,
            'image_path': self.image_path,
            'options': [opt.to_dict() for opt in self.options]
        }

class QuestionOption(db.Model):
    __tablename__ = 'question_options'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id', ondelete='CASCADE'), nullable=False)
    option_text = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'option_text': self.option_text,
            'is_correct': self.is_correct
        }

class LearningRecord(db.Model):
    __tablename__ = 'learning_records'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.String(50), db.ForeignKey('employees.id', ondelete='CASCADE'), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id', ondelete='CASCADE'), nullable=False)
    study_time = db.Column(db.Integer, default=0) # in seconds
    pass_rate = db.Column(db.Float, default=0.0)
    accuracy = db.Column(db.Float, default=0.0)
    max_combo = db.Column(db.Integer, default=0)
    xp_gained = db.Column(db.Integer, default=0)
    study_date = db.Column(db.Date, default=datetime.utcnow().date)

    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'lesson_id': self.lesson_id,
            'study_time': self.study_time,
            'pass_rate': self.pass_rate,
            'accuracy': self.accuracy,
            'max_combo': self.max_combo,
            'xp_gained': self.xp_gained,
            'study_date': self.study_date.isoformat()
        }

class WrongQuestion(db.Model):
    __tablename__ = 'wrong_questions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.String(50), db.ForeignKey('employees.id', ondelete='CASCADE'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id', ondelete='CASCADE'), nullable=False)
    wrong_count = db.Column(db.Integer, default=1)
    recall_count = db.Column(db.Integer, default=0)
    last_wrong_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    question = db.relationship('Question', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'question_id': self.question_id,
            'wrong_count': self.wrong_count,
            'recall_count': self.recall_count,
            'last_wrong_at': self.last_wrong_at.isoformat() if self.last_wrong_at else None,
            'question_details': self.question.to_dict() if self.question else None
        }

class Badge(db.Model):
    __tablename__ = 'badges'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    icon_path = db.Column(db.String(255), nullable=True)
    trigger_type = db.Column(db.String(50), nullable=False) # 'first_pass', 'streak_7', etc.

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'icon_path': self.icon_path,
            'trigger_type': self.trigger_type
        }

class EmployeeBadge(db.Model):
    __tablename__ = 'employee_badges'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.String(50), db.ForeignKey('employees.id', ondelete='CASCADE'), nullable=False)
    badge_id = db.Column(db.Integer, db.ForeignKey('badges.id', ondelete='CASCADE'), nullable=False)
    earned_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    badge = db.relationship('Badge', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'badge_id': self.badge_id,
            'earned_at': self.earned_at.isoformat() if self.earned_at else None,
            'badge_details': self.badge.to_dict() if self.badge else None
        }

class LanguageReport(db.Model):
    __tablename__ = 'language_reports'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.String(50), db.ForeignKey('employees.id', ondelete='CASCADE'), nullable=False, unique=True)
    level = db.Column(db.String(10), default='A1')
    score_vocabulary = db.Column(db.Float, default=0.0)
    score_grammar = db.Column(db.Float, default=0.0)
    score_dialogue = db.Column(db.Float, default=0.0)
    score_safety = db.Column(db.Float, default=0.0)
    score_work = db.Column(db.Float, default=0.0)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'level': self.level,
            'score_vocabulary': self.score_vocabulary,
            'score_grammar': self.score_grammar,
            'score_dialogue': self.score_dialogue,
            'score_safety': self.score_safety,
            'score_work': self.score_work,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class SystemLog(db.Model):
    __tablename__ = 'system_logs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    level = db.Column(db.String(20), nullable=False)
    operator = db.Column(db.String(100), nullable=True)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'level': self.level,
            'operator': self.operator,
            'message': self.message,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
