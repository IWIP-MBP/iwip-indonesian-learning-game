SET NAMES utf8mb4;
-- Create Database
CREATE DATABASE IF NOT EXISTS iwip_indonesian CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE iwip_indonesian;

-- 1. Departments Table
CREATE TABLE IF NOT EXISTS departments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 2. Employees Table
CREATE TABLE IF NOT EXISTS employees (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    department_id INT,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'employee',
    xp INT DEFAULT 0,
    level INT DEFAULT 1,
    FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 3. Lessons Table
CREATE TABLE IF NOT EXISTS lessons (
    id INT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL -- 'pronunciation' or 'regular'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 4. Vocabulary Table
CREATE TABLE IF NOT EXISTS vocabulary (
    id INT AUTO_INCREMENT PRIMARY KEY,
    lesson_id INT NOT NULL,
    word VARCHAR(255) NOT NULL,
    translation VARCHAR(255) NOT NULL,
    phonetic VARCHAR(255) NULL,
    audio_path VARCHAR(255) NULL,
    FOREIGN KEY (lesson_id) REFERENCES lessons(id) ON DELETE CASCADE,
    INDEX idx_lesson_vocab (lesson_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 5. Sentences (Examples) Table
CREATE TABLE IF NOT EXISTS sentences (
    id INT AUTO_INCREMENT PRIMARY KEY,
    lesson_id INT NOT NULL,
    indonesian TEXT NOT NULL,
    chinese TEXT NOT NULL,
    FOREIGN KEY (lesson_id) REFERENCES lessons(id) ON DELETE CASCADE,
    INDEX idx_lesson_sentences (lesson_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 6. Dialogues Table
CREATE TABLE IF NOT EXISTS dialogues (
    id INT AUTO_INCREMENT PRIMARY KEY,
    lesson_id INT NOT NULL,
    dialogue_group INT NOT NULL,
    speaker VARCHAR(50) NULL,
    indonesian TEXT NOT NULL,
    chinese TEXT NOT NULL,
    FOREIGN KEY (lesson_id) REFERENCES lessons(id) ON DELETE CASCADE,
    INDEX idx_lesson_dialogues (lesson_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 7. Grammar Table
CREATE TABLE IF NOT EXISTS grammar (
    id INT AUTO_INCREMENT PRIMARY KEY,
    lesson_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    FOREIGN KEY (lesson_id) REFERENCES lessons(id) ON DELETE CASCADE,
    INDEX idx_lesson_grammar (lesson_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 8. Questions Table
CREATE TABLE IF NOT EXISTS questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    lesson_id INT NOT NULL,
    type VARCHAR(50) NOT NULL, -- 'vocab_choice', 'cn_to_indo', 'indo_to_cn', 'audio', 'picture', 'fill_blank', 'dialogue', 'drag_match'
    content TEXT NOT NULL,
    explanation TEXT NULL,
    audio_path VARCHAR(255) NULL,
    image_path VARCHAR(255) NULL,
    FOREIGN KEY (lesson_id) REFERENCES lessons(id) ON DELETE CASCADE,
    INDEX idx_lesson_questions (lesson_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 9. Question Options Table
CREATE TABLE IF NOT EXISTS question_options (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question_id INT NOT NULL,
    option_text TEXT NOT NULL,
    is_correct BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE,
    INDEX idx_question_options (question_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 10. Learning Records Table
CREATE TABLE IF NOT EXISTS learning_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id VARCHAR(50) NOT NULL,
    lesson_id INT NOT NULL,
    study_time INT DEFAULT 0, -- in seconds
    pass_rate FLOAT DEFAULT 0.0,
    accuracy FLOAT DEFAULT 0.0,
    max_combo INT DEFAULT 0,
    xp_gained INT DEFAULT 0,
    study_date DATE NOT NULL,
    FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE,
    FOREIGN KEY (lesson_id) REFERENCES lessons(id) ON DELETE CASCADE,
    INDEX idx_emp_record (employee_id),
    INDEX idx_lesson_record (lesson_id),
    INDEX idx_study_date (study_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 11. Wrong Questions Table
CREATE TABLE IF NOT EXISTS wrong_questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id VARCHAR(50) NOT NULL,
    question_id INT NOT NULL,
    wrong_count INT DEFAULT 1,
    last_wrong_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE,
    FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE,
    UNIQUE KEY uq_emp_question (employee_id, question_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 12. Badges Table
CREATE TABLE IF NOT EXISTS badges (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT NULL,
    icon_path VARCHAR(255) NULL,
    trigger_type VARCHAR(50) NOT NULL -- 'first_pass', 'streak_7', 'streak_30', 'vocab_master', 'work_master', 'safety_master', 'translation_master'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 13. Employee Badges Table
CREATE TABLE IF NOT EXISTS employee_badges (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id VARCHAR(50) NOT NULL,
    badge_id INT NOT NULL,
    earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE,
    FOREIGN KEY (badge_id) REFERENCES badges(id) ON DELETE CASCADE,
    UNIQUE KEY uq_emp_badge (employee_id, badge_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 14. Language Reports (Capability Analysis) Table
CREATE TABLE IF NOT EXISTS language_reports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id VARCHAR(50) NOT NULL UNIQUE,
    level VARCHAR(10) DEFAULT 'A1', -- 'A1', 'A2', 'B1', 'B2', 'C1', 'C2'
    score_vocabulary FLOAT DEFAULT 0.0,
    score_grammar FLOAT DEFAULT 0.0,
    score_dialogue FLOAT DEFAULT 0.0,
    score_safety FLOAT DEFAULT 0.0,
    score_work FLOAT DEFAULT 0.0,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 15. System Logs Table
CREATE TABLE IF NOT EXISTS system_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    level VARCHAR(20) NOT NULL,
    operator VARCHAR(100) NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Seed default departments (removed pre-seeded departments)

-- Seed default admin account (password_hash is pbkdf2:sha256:600000$admin123_hash or similar, we will handle hash check in backend, let's write a standard hash for 'admin123')
-- pbkdf2:sha256:600000$admin123$ef48d28a38a7c29fb1e3d3ff6987f6ee6a9b400787e974e64f84c40590a53b58 (simulated pbkdf2 hash)
INSERT INTO employees (id, name, department_id, password_hash, role) 
VALUES ('admin', '管理员', NULL, 'scrypt:32768:8:1$WK7dJvmUv0YXSYmQ$36e4274ff6921554dd3df10941c8431af2d13900067c704548e18d9a4a64d29eb5eeafd02631fa45d0c3e53b32085a0ef44dc3676979742cf57f097b47a42e54', 'admin');

-- Seed default badges
INSERT INTO badges (name, description, icon_path, trigger_type) VALUES
('开端', '首次通过任意课程', 'first_pass.png', 'first_pass'),
('持之以恒', '连续学习7天', 'streak_7.png', 'streak_7'),
('铁杆粉', '连续学习30天', 'streak_30.png', 'streak_30'),
('词汇达人', '掌握超过100个印尼语单词', 'vocab_master.png', 'vocab_master'),
('办公达人', '完成所有办公场景课程', 'work_master.png', 'work_master'),
('安全达人', '完成所有安全场景课程并满分', 'safety_master.png', 'safety_master'),
('翻译达人', '做对50道翻译及例句题', 'translation_master.png', 'translation_master');
