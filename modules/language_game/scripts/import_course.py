import os
import re
import json
import fitz  # PyMuPDF

def extract_pdf_content(pdf_path):
    doc = fitz.open(pdf_path)
    pages_text = []
    for page in doc:
        pages_text.append(page.get_text())
    return pages_text

def parse_global_vocabulary(pages):
    global_vocab = []
    # pages 86 to 93 are indices 85 to 92 (inclusive)
    for p_idx in range(85, 93):
        if p_idx >= len(pages):
            continue
        text = pages[p_idx]
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        
        if p_idx == 85:
            lines = [l for l in lines if l not in ["初级单词表", "KURSUS PELATIHAN BAHASA INDONESIA", "印尼语培训课程"]]
            
        i = 0
        while i < len(lines):
            line = lines[i]
            if len(line) == 1 and line.isalpha():
                i += 1
                continue
            
            if i + 1 < len(lines):
                word = line
                translation = lines[i+1]
                
                is_indo = re.match(r"^[a-zA-Z\s\-\.\'\,\/\(\)\:\!\?\’\”]+$", word)
                is_cn = re.search(r"[\u4e00-\u9fff]", translation)
                
                if is_indo and is_cn:
                    global_vocab.append({
                        "word": word.strip(),
                        "translation": translation.strip(),
                        "phonetic": None
                    })
                    i += 2
                else:
                    i += 1
            else:
                i += 1
    return global_vocab

def parse_course(pdf_path):
    pages = extract_pdf_content(pdf_path)
    
    # Define lessons with page ranges (0-indexed)
    lessons_config = [
        {"id": 1, "title": "发音（一） Pelafalan 1", "type": "pronunciation", "pages": range(1, 4)},
        {"id": 2, "title": "发音（二） Pelafalan 2", "type": "pronunciation", "pages": range(4, 8)},
        {"id": 3, "title": "发音（三） Pelafalan 3", "type": "pronunciation", "pages": range(8, 12)},
        {"id": 4, "title": "发音（四） Pelafalan 4", "type": "pronunciation", "pages": range(12, 18)},
        {"id": 5, "title": "发音（五） Pelafalan 5", "type": "pronunciation", "pages": range(18, 21)},
        {"id": 6, "title": "发音（六） Pelafalan 6", "type": "pronunciation", "pages": range(21, 23)},
        {"id": 7, "title": "发音（七） Pelafalan 7", "type": "pronunciation", "pages": range(23, 27)},
        {"id": 8, "title": "发音（八） Pelafalan 8", "type": "pronunciation", "pages": range(27, 29)},
        {"id": 9, "title": "第九课- 语法 Pelajaran ke-9: Tata Bahasa", "type": "regular", "pages": range(29, 31)},
        {"id": 10, "title": "第十课- 我的爱好 Pelajaran ke-10: Hobi Saya", "type": "regular", "pages": range(31, 35)},
        {"id": 11, "title": "第十一课- 自我介绍 Pelajaran ke-11: Memperkenalkan Diri", "type": "regular", "pages": range(35, 38)},
        {"id": 12, "title": "第十二课- 日期 Pelajaran ke-12: Tanggal", "type": "regular", "pages": range(38, 41)},
        {"id": 13, "title": "第十三课- 天气 Pelajaran ke-13: Cuaca", "type": "regular", "pages": range(41, 45)},
        {"id": 14, "title": "第十四课- 超市 Pelajaran ke-14: Swalayan", "type": "regular", "pages": range(45, 49)},
        {"id": 15, "title": "第十五课- 食堂 Pelajaran ke-15: Kantin", "type": "regular", "pages": range(49, 53)},
        {"id": 16, "title": "第十六课- 宿舍 Pelajaran ke-16: Asrama", "type": "regular", "pages": range(53, 57)},
        {"id": 17, "title": "第十七课- 生病 Pelajaran ke-17: Sakit", "type": "regular", "pages": range(57, 62)},
        {"id": 18, "title": "第十八课- 续签与休假 Pelajaran ke-18: Visa dan Cuti", "type": "regular", "pages": range(62, 66)},
        {"id": 19, "title": "第十九课- 安全与健康 Pelajaran ke-19: Keselamatan dan Kesehatan", "type": "regular", "pages": range(66, 69)},
        {"id": 20, "title": "第二十课- 工作环境（办公室） Pelajaran ke-20: Lingkungan Kerja (Kantor)", "type": "regular", "pages": range(69, 72)},
        {"id": 21, "title": "第二十一课- 工作环境（现场） Pelajaran ke-21: Lingkungan Kerja (Lapangan)", "type": "regular", "pages": range(72, 76)},
    ]
    
    parsed_lessons = []
    
    for l_conf in lessons_config:
        lesson_id = l_conf["id"]
        title = l_conf["title"]
        l_type = l_conf["type"]
        
        lesson_data = {
            "id": lesson_id,
            "title": title,
            "type": l_type,
            "vocabulary": [],
            "sentences": [],
            "dialogues": [],
            "grammar": []
        }
        
        lesson_text = ""
        for p_idx in l_conf["pages"]:
            if p_idx < len(pages):
                lesson_text += pages[p_idx] + "\n"
        
        lines = [line.strip() for line in lesson_text.split("\n") if line.strip()]
        
        mode = "NONE"
        
        i = 0
        while i < len(lines):
            line = lines[i]
            
            if "KOSAKATA" in line or "单词" in line:
                mode = "VOCAB"
                i += 1
                continue
            elif "CONTOH KALIMAT" in line or "例句" in line or "TERJEMAHKAN" in line or "翻译" in line or "LATIHAN" in line:
                mode = "SENTENCE"
                i += 1
                continue
            elif "PERCAKAPAN" in line or "对话" in line or "Percakapan" in line:
                mode = "DIALOGUE"
                i += 1
                continue
            elif "TATA BAHASA" in line or "语法" in line:
                mode = "GRAMMAR"
                i += 1
                continue
            
            if mode == "VOCAB":
                vocab_num_match = re.match(r"^(\d+)\.\s*(.*)$", line)
                if vocab_num_match:
                    num = vocab_num_match.group(1)
                    word = vocab_num_match.group(2).strip()
                    
                    if not word:
                        if i + 1 < len(lines):
                            word = lines[i+1]
                            if i + 2 < len(lines):
                                translation = lines[i+2]
                                i += 3
                            else:
                                translation = ""
                                i += 2
                        else:
                            word = ""
                            translation = ""
                            i += 1
                    else:
                        if i + 1 < len(lines):
                            translation = lines[i+1]
                            i += 2
                        else:
                            translation = ""
                            i += 1
                            
                    if word and translation:
                        word = re.sub(r"^\d+\.?\s*", "", word).strip()
                        translation = re.sub(r"^\d+\.?\s*", "", translation).strip()
                        lesson_data["vocabulary"].append({
                            "word": word,
                            "translation": translation,
                            "phonetic": None
                        })
                    continue
                else:
                    if l_type == "pronunciation" and not line.startswith("=== PAGE"):
                        is_indo = re.match(r"^[a-zA-Z\s\-\.\'\,\/]+$", line)
                        if is_indo and i + 1 < len(lines):
                            next_line = lines[i+1]
                            is_cn = re.search(r"[\u4e00-\u9fff]", next_line)
                            if is_cn:
                                lesson_data["vocabulary"].append({
                                    "word": line,
                                    "translation": next_line,
                                    "phonetic": None
                                })
                                i += 2
                                continue
                
            elif mode == "SENTENCE":
                sent_match = re.match(r"^(\d+)\.\s*(.*)$", line)
                if sent_match:
                    num = sent_match.group(1)
                    indo_sent = sent_match.group(2).strip()
                    if not indo_sent:
                        if i + 1 < len(lines):
                            indo_sent = lines[i+1]
                            if i + 2 < len(lines):
                                cn_sent = lines[i+2]
                                i += 3
                            else:
                                cn_sent = ""
                                i += 2
                        else:
                            indo_sent = ""
                            cn_sent = ""
                            i += 1
                    else:
                        if i + 1 < len(lines):
                            cn_sent = lines[i+1]
                            i += 2
                        else:
                            cn_sent = ""
                            i += 1
                    
                    if indo_sent:
                        lesson_data["sentences"].append({
                            "indonesian": indo_sent,
                            "chinese": cn_sent
                        })
                    continue
                    
            elif mode == "DIALOGUE":
                dial_match = re.match(r"^([a-zA-Z\s]+):\s*(.*)$", line)
                if dial_match:
                    speaker = dial_match.group(1).strip()
                    indo_text = dial_match.group(2).strip()
                    if not indo_text:
                        if i + 1 < len(lines):
                            indo_text = lines[i+1]
                            if i + 2 < len(lines):
                                cn_text = lines[i+2]
                                i += 3
                            else:
                                cn_text = ""
                                i += 2
                        else:
                            indo_text = ""
                            cn_text = ""
                            i += 1
                    else:
                        if i + 1 < len(lines):
                            cn_text = lines[i+1]
                            i += 2
                        else:
                            cn_text = ""
                            i += 1
                    
                    if indo_text:
                        lesson_data["dialogues"].append({
                            "speaker": speaker,
                            "indonesian": indo_text,
                            "chinese": cn_text,
                            "dialogue_group": 1
                        })
                    continue
            
            elif mode == "GRAMMAR":
                if not line.startswith("===") and len(line) > 2:
                    lesson_data["grammar"].append(line)
            
            i += 1
            
        if lesson_data["grammar"]:
            combined_grammar = "\n".join(lesson_data["grammar"])
            lesson_data["grammar"] = [{
                "title": "语法详解",
                "content": combined_grammar
            }]
            
        parsed_lessons.append(lesson_data)
        
    # Parse global vocabulary and distribute to lessons with few words
    global_vocab = parse_global_vocabulary(pages)
    
    # Assign global vocabulary as supplementary vocabulary to lessons
    # Distribute them evenly to ensure each lesson has at least 30-40 words
    words_per_lesson = len(global_vocab) // len(lessons_config)
    for idx, lesson in enumerate(parsed_lessons):
        start_idx = idx * words_per_lesson
        end_idx = start_idx + words_per_lesson
        if idx == len(parsed_lessons) - 1:
            end_idx = len(global_vocab)
        
        supp_words = global_vocab[start_idx:end_idx]
        
        # Merge, checking for duplicates
        existing_words = {w["word"].lower() for w in lesson["vocabulary"]}
        for w in supp_words:
            if w["word"].lower() not in existing_words:
                lesson["vocabulary"].append(w)
                existing_words.add(w["word"].lower())
                
    return {
        "lessons": parsed_lessons,
        "global_vocabulary": global_vocab
    }

def main():
    pdf_path = r"d:\STUDY\印尼语.pdf"
    print("Parsing PDF course textbook...")
    data = parse_course(pdf_path)
    
    output_dir = r"d:\STUDY\modules\language_game\database"
    os.makedirs(output_dir, exist_ok=True)
    json_path = os.path.join(output_dir, "parsed_course.json")
    
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    print(f"Parsing complete! Saved data to {json_path}")
    print(f"Total global vocabulary items parsed: {len(data['global_vocabulary'])}")
    
    for lesson in data["lessons"]:
        print(f"Lesson {lesson['id']}: {lesson['title']} - Total Vocab (after distribution): {len(lesson['vocabulary'])}, Sentences: {len(lesson['sentences'])}, Dialogues: {len(lesson['dialogues'])}, Grammar: {len(lesson['grammar'])}")

if __name__ == "__main__":
    main()
