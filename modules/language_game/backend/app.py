import os
import json
from flask import Flask, jsonify
from flask_cors import CORS
from .models import db, Lesson, Vocabulary, Sentence, Dialogue, Grammar, Question, QuestionOption, Employee, Department, LanguageReport
from . import language_game_bp

def create_app(test_config=None):
    app = Flask(__name__)
    
    # Enable CORS
    CORS(app)
    
    # Configure database
    # Connect to MySQL if environment variables are set, fallback to local SQLite for easy development
    mysql_host = os.environ.get('MYSQL_HOST', 'localhost')
    mysql_port = os.environ.get('MYSQL_PORT', '3306')
    mysql_db = os.environ.get('MYSQL_DATABASE', 'iwip_indonesian')
    mysql_user = os.environ.get('MYSQL_USER', 'root')
    mysql_pass = os.environ.get('MYSQL_PASSWORD', 'root1234')
    
    # Check if we should use MySQL or local SQLite
    if os.environ.get('USE_SQLITE') == 'true' or not os.environ.get('MYSQL_HOST'):
        db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'iwip.db')
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
        print(f"Database: Using SQLite at {db_path}")
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{mysql_user}:{mysql_pass}@{mysql_host}:{mysql_port}/{mysql_db}?charset=utf8mb4'
        print(f"Database: Using MySQL at {mysql_host}:{mysql_port}")
        
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'iwip_secret_start_key_123')
    
    db.init_app(app)
    
    # Register language game blueprint
    app.register_blueprint(language_game_bp, url_prefix='/api')
    
    # Setup startup/seeding hooks
    @app.cli.command("seed-db")
    def seed_db_command():
        seed_database(app)
        
    # Health check route
    @app.route('/health')
    def health():
        return jsonify({'status': 'healthy', 'service': 'iwip-backend'}), 200
        
    return app

def seed_database(app):
    with app.app_context():
        print("Starting Database Seeding...")
        db.create_all()
        
        # 1. Seed Default Admin Employee
        admin_user = Employee.query.get('admin')
        if not admin_user:
            # We seed administration department
            admin_dept = Department.query.filter_by(name='管理层').first()
            if not admin_dept:
                admin_dept = Department(name='管理层')
                db.session.add(admin_dept)
                db.session.commit()
            
            admin_user = Employee(
                id='admin',
                name='系统管理员',
                department_id=admin_dept.id,
                role='admin'
            )
            # Default password is 'admin123'
            admin_user.set_password('admin123')
            db.session.add(admin_user)
            
            # Create report card
            rep = LanguageReport(employee_id='admin')
            db.session.add(rep)
            db.session.commit()
            print("Seeded default admin user 'admin' / 'admin123'")
        else:
            # If admin exists with the dummy hash from init.sql, update it to the correct hash
            if admin_user.password_hash == 'pbkdf2:sha256:600000$salt123$f25e985b8813bc6e6f987f6ee6a9b400787e974e64f84c40590a53b58':
                admin_user.set_password('admin123')
                db.session.commit()
                print("Corrected dummy admin password hash to valid 'admin123' hash.")
            
        # 2. Check if Lessons are empty, seed from parsed_course.json
        if Lesson.query.first() is None:
            json_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../database/parsed_course.json'))
            if os.path.exists(json_path):
                print(f"Seeding course data from {json_path}...")
                with open(json_path, 'r', encoding='utf-8') as f:
                    course_data = json.load(f)
                    
                lessons_list = course_data if isinstance(course_data, list) else course_data.get('lessons', [])
                
                for les in lessons_list:
                    lesson = Lesson(
                        id=les['id'],
                        title=les['title'],
                        type=les['type']
                    )
                    db.session.add(lesson)
                    
                    # Vocabs
                    for item in les.get('vocabulary', []):
                        vocab = Vocabulary(
                            lesson_id=les['id'],
                            word=item['word'],
                            translation=item['translation'],
                            phonetic=item.get('phonetic'),
                            audio_path=item.get('audio_path')
                        )
                        db.session.add(vocab)
                        
                    # Sentences
                    for item in les.get('sentences', []):
                        sent = Sentence(
                            lesson_id=les['id'],
                            indonesian=item['indonesian'],
                            chinese=item['chinese']
                        )
                        db.session.add(sent)
                        
                    # Dialogues
                    for item in les.get('dialogues', []):
                        dial = Dialogue(
                            lesson_id=les['id'],
                            dialogue_group=item['dialogue_group'],
                            speaker=item.get('speaker'),
                            indonesian=item['indonesian'],
                            chinese=item['chinese']
                        )
                        db.session.add(dial)
                        
                    # Grammar
                    for item in les.get('grammar', []):
                        gram = Grammar(
                            lesson_id=les['id'],
                            title=item['title'],
                            content=item['content']
                        )
                        db.session.add(gram)
                        
                db.session.commit()
                print("Seeded all 21 lessons, vocabulary, sentences, dialogues, and grammar successfully!")
            else:
                print(f"Warning: Course JSON file not found at {json_path}")
                
        # 3. Check if Questions are empty, seed from generated_questions.json
        if Question.query.first() is None:
            json_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../database/generated_questions.json'))
            if os.path.exists(json_path):
                print(f"Seeding 3000+ questions from {json_path}...")
                with open(json_path, 'r', encoding='utf-8') as f:
                    questions_data = json.load(f)
                    
                for q in questions_data:
                    question = Question(
                        id=q['id'],
                        lesson_id=q['lesson_id'],
                        type=q['type'],
                        content=q['content'],
                        explanation=q.get('explanation'),
                        audio_path=q.get('audio_path'),
                        image_path=q.get('image_path')
                    )
                    db.session.add(question)
                    
                    # Seed Options
                    for opt in q.get('options', []):
                        option = QuestionOption(
                            question_id=q['id'],
                            option_text=opt['text'],
                            is_correct=opt['is_correct']
                        )
                        db.session.add(option)
                        
                db.session.commit()
                print(f"Seeded {len(questions_data)} questions and their options successfully!")
            else:
                print(f"Warning: Questions JSON file not found at {json_path}")
                
        print("Database Seeding Finished!")

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
        seed_database(app)
    app.run(host='0.0.0.0', port=5000, debug=True)
