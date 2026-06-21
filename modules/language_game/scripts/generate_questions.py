import os
import json
import random
import re

def generate_vocab_choice(word_list, index, question_id_counter, lesson_id):
    word_item = word_list[index]
    word = word_item["word"]
    translation = word_item["translation"]
    
    # Select distractors from other words in the same list
    other_words = [w for w in word_list if w["word"] != word]
    if len(other_words) < 3:
        # Fallback to general list if not enough words
        other_words = word_list
        
    distractors = random.sample(other_words, min(3, len(other_words)))
    
    options = [{"text": translation, "is_correct": True}]
    for d in distractors:
        options.append({"text": d["translation"], "is_correct": False})
    
    # Shuffle options
    random.shuffle(options)
    
    return {
        "id": question_id_counter,
        "lesson_id": lesson_id,
        "type": "vocab_choice",
        "content": f"单词“{word}”的中文意思是什么？",
        "options": options,
        "explanation": f"印尼语单词“{word}”的中文意思是“{translation}”。"
    }

def generate_cn_to_indo(word_list, index, question_id_counter, lesson_id):
    word_item = word_list[index]
    word = word_item["word"]
    translation = word_item["translation"]
    
    other_words = [w for w in word_list if w["word"] != word]
    if len(other_words) < 3:
        other_words = word_list
        
    distractors = random.sample(other_words, min(3, len(other_words)))
    
    options = [{"text": word, "is_correct": True}]
    for d in distractors:
        options.append({"text": d["word"], "is_correct": False})
        
    random.shuffle(options)
    
    return {
        "id": question_id_counter,
        "lesson_id": lesson_id,
        "type": "cn_to_indo",
        "content": f"中文“{translation}”对应的印尼语单词是什么？",
        "options": options,
        "explanation": f"中文“{translation}”对应的印尼语单词是“{word}”。"
    }

def generate_indo_to_cn(word_list, index, question_id_counter, lesson_id):
    word_item = word_list[index]
    word = word_item["word"]
    translation = word_item["translation"]
    
    other_words = [w for w in word_list if w["word"] != word]
    if len(other_words) < 3:
        other_words = word_list
        
    distractors = random.sample(other_words, min(3, len(other_words)))
    
    options = [{"text": translation, "is_correct": True}]
    for d in distractors:
        options.append({"text": d["translation"], "is_correct": False})
        
    random.shuffle(options)
    
    return {
        "id": question_id_counter,
        "lesson_id": lesson_id,
        "type": "indo_to_cn",
        "content": f"选择正确的中文翻译：\n【 {word} 】",
        "options": options,
        "explanation": f"“{word}”翻译成中文是“{translation}”。"
    }

def generate_audio_question(word_list, index, question_id_counter, lesson_id):
    word_item = word_list[index]
    word = word_item["word"]
    translation = word_item["translation"]
    
    other_words = [w for w in word_list if w["word"] != word]
    if len(other_words) < 3:
        other_words = word_list
        
    distractors = random.sample(other_words, min(3, len(other_words)))
    
    options = [{"text": translation, "is_correct": True}]
    for d in distractors:
        options.append({"text": d["translation"], "is_correct": False})
        
    random.shuffle(options)
    
    return {
        "id": question_id_counter,
        "lesson_id": lesson_id,
        "type": "audio",
        "content": word, # The word to be pronounced by TTS
        "options": options,
        "explanation": f"听音辨义：印尼语发音的单词是“{word}”，意思是“{translation}”。"
    }

def generate_picture_question(word_list, index, question_id_counter, lesson_id):
    word_item = word_list[index]
    word = word_item["word"]
    translation = word_item["translation"]
    
    other_words = [w for w in word_list if w["word"] != word]
    if len(other_words) < 3:
        other_words = word_list
        
    distractors = random.sample(other_words, min(3, len(other_words)))
    
    options = [{"text": word, "is_correct": True}]
    for d in distractors:
        options.append({"text": d["word"], "is_correct": False})
        
    random.shuffle(options)
    
    # We map specific words to premium visual assets
    # Fallback to a general category illustration
    img_name = word.lower().replace(" ", "_").replace("/", "_")
    image_path = f"/assets/images/quiz/{img_name}.png"
    
    return {
        "id": question_id_counter,
        "lesson_id": lesson_id,
        "type": "picture",
        "content": f"请选择与图片相对应的印尼语单词：",
        "image_path": image_path,
        "options": options,
        "explanation": f"图片展示的是“{translation}”，对应的印尼语单词是“{word}”。"
    }

def generate_fill_blank(word_list, sentences, index, question_id_counter, lesson_id):
    if sentences:
        sent_item = sentences[index % len(sentences)]
        indo = sent_item["indonesian"]
        cn = sent_item["chinese"]
        
        # Split sentence into words and find a word to mask
        words = re.findall(r"\b[a-zA-Z\d\-]+\b", indo)
        
        # Try to find a word in words that matches one of our vocabulary items
        masked_word = None
        for w in words:
            if any(vi["word"].lower() == w.lower() for vi in word_list):
                masked_word = w
                break
                
        if not masked_word and words:
            masked_word = random.choice(words)
            
        if masked_word:
            masked_indo = re.sub(r"\b" + re.escape(masked_word) + r"\b", "_______", indo)
            
            # Find distractors
            other_words = [vi["word"] for vi in word_list if vi["word"].lower() != masked_word.lower()]
            if len(other_words) < 3:
                other_words = ["di", "saya", "kamu", "ini", "itu", "ada", "apa"]
            distractors = random.sample(other_words, min(3, len(other_words)))
            
            options = [{"text": masked_word, "is_correct": True}]
            for d in distractors:
                options.append({"text": d, "is_correct": False})
                
            random.shuffle(options)
            
            return {
                "id": question_id_counter,
                "lesson_id": lesson_id,
                "type": "fill_blank",
                "content": f"补全句子：\n{masked_indo}\n（中文释义：{cn}）",
                "options": options,
                "explanation": f"本句意为“{cn}”。这里需要填入印尼语单词“{masked_word}”。完整句子是：{indo}。"
            }
            
    # Fallback for spelling/pronunciation blank questions
    word_item = word_list[index % len(word_list)]
    word = word_item["word"]
    translation = word_item["translation"]
    
    if len(word) >= 3:
        # Mask a vowel or letter
        mask_idx = random.randint(1, len(word) - 2)
        masked_char = word[mask_idx]
        masked_word = word[:mask_idx] + "_" + word[mask_idx+1:]
        
        distractors = [c for c in ["a", "i", "u", "e", "o"] if c != masked_char.lower()]
        options = [{"text": masked_char, "is_correct": True}]
        for d in distractors[:3]:
            options.append({"text": d, "is_correct": False})
            
        random.shuffle(options)
        
        return {
            "id": question_id_counter,
            "lesson_id": lesson_id,
            "type": "fill_blank",
            "content": f"请补全单词拼写：\n【 {masked_word} 】\n（中文释义：{translation}）",
            "options": options,
            "explanation": f"印尼语单词“{word}”意为“{translation}”，缺失的字母是“{masked_char}”。"
        }
    else:
        # Fallback to simple grammar check
        options = [
            {"text": "di", "is_correct": True},
            {"text": "ke", "is_correct": False},
            {"text": "dari", "is_correct": False},
            {"text": "ini", "is_correct": False}
        ]
        random.shuffle(options)
        return {
            "id": question_id_counter,
            "lesson_id": lesson_id,
            "type": "fill_blank",
            "content": f"Saya ____ sini. （我在这里。）",
            "options": options,
            "explanation": f"表达在某处应该使用介词“di”。正确句子是“Saya di sini.”。"
        }

def generate_dialogue_question(word_list, dialogues, index, question_id_counter, lesson_id):
    if dialogues:
        # Select a dialogue
        dial_item = dialogues[index % len(dialogues)]
        speaker = dial_item["speaker"]
        indo = dial_item["indonesian"]
        cn = dial_item["chinese"]
        
        # We mask the response or question
        content = f"根据对话选择合适的回复：\n【 对方问：{indo} ({cn}) 】"
        
        # Correct answer is the next dialogue line, or a fitting phrase
        # Let's find other dialogue lines from the same lesson as distractors
        other_dials = [d for d in dialogues if d["indonesian"] != indo]
        if other_dials:
            correct_item = other_dials[0]
            correct_text = f"{correct_item['speaker']}: {correct_item['indonesian']} ({correct_item['chinese']})"
            distractors = []
            for od in other_dials[1:4]:
                distractors.append(f"{od['speaker']}: {od['indonesian']} ({od['chinese']})")
        else:
            correct_text = "Saya di sini. (我在这里。)"
            distractors = [
                "Nama saya Tata. (我的名字是Tata。)",
                "Apa ini? (这是什么？)",
                "Saya di sana. (我在那里。)"
            ]
            
        options = [{"text": correct_text, "is_correct": True}]
        for d in distractors:
            options.append({"text": d, "is_correct": False})
        random.shuffle(options)
        
        return {
            "id": question_id_counter,
            "lesson_id": lesson_id,
            "type": "dialogue",
            "content": content,
            "options": options,
            "explanation": f"对话完成：合适的回复是“{correct_text}”。"
        }
        
    # Fallback dialog match
    options = [
        {"text": "Nama saya Tata. (我的名字是Tata。)", "is_correct": True},
        {"text": "Saya di asrama. (我在宿舍。)", "is_correct": False},
        {"text": "AC rusak. (空调坏了。)", "is_correct": False},
        {"text": "Sama-sama. (不客气。)", "is_correct": False}
    ]
    random.shuffle(options)
    return {
        "id": question_id_counter,
        "lesson_id": lesson_id,
        "type": "dialogue",
        "content": "根据上下文选择最合适的回复：\n【 A: Siapa nama kamu? (你叫什么名字？) 】",
        "options": options,
        "explanation": f"当别人问姓名时，应该回复“Nama saya Tata.”。"
    }

def generate_drag_match(word_list, question_id_counter, lesson_id):
    # Select 4 pairs
    pairs = random.sample(word_list, min(4, len(word_list)))
    content_pairs = [{"indo": p["word"], "cn": p["translation"]} for p in pairs]
    
    return {
        "id": question_id_counter,
        "lesson_id": lesson_id,
        "type": "drag_match",
        "content": json.dumps(content_pairs, ensure_ascii=False),
        "options": [], # Drag match doesn't have options, verified client-side
        "explanation": "拖拽匹配：请将对应的印尼语单词和中文含义配对连线。"
    }

def main():
    json_path = r"d:\STUDY\modules\language_game\database\parsed_course.json"
    if not os.path.exists(json_path):
        print(f"Error: parsed course JSON not found at {json_path}")
        return
        
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    lessons = data["lessons"]
    
    questions_bank = []
    question_id_counter = 1
    
    print("Generating question bank...")
    
    for lesson in lessons:
        lesson_id = lesson["id"]
        vocab = lesson["vocabulary"]
        sentences = lesson["sentences"]
        dialogues = lesson["dialogues"]
        
        # We need to generate exactly 150 questions for each lesson
        # to guarantee >= 100 questions per lesson, and total >= 3000 questions (21 * 150 = 3150)
        num_vocab_choice = 30
        num_cn_to_indo = 30
        num_indo_to_cn = 30
        num_audio = 20
        num_picture = 10
        num_fill_blank = 20
        num_dialogue = 5
        num_drag_match = 5
        
        # 1. Vocab Choice
        for idx in range(num_vocab_choice):
            word_idx = idx % len(vocab)
            q = generate_vocab_choice(vocab, word_idx, question_id_counter, lesson_id)
            questions_bank.append(q)
            question_id_counter += 1
            
        # 2. Chinese to Indonesian
        for idx in range(num_cn_to_indo):
            word_idx = idx % len(vocab)
            q = generate_cn_to_indo(vocab, word_idx, question_id_counter, lesson_id)
            questions_bank.append(q)
            question_id_counter += 1
            
        # 3. Indonesian to Chinese
        for idx in range(num_indo_to_cn):
            word_idx = idx % len(vocab)
            q = generate_indo_to_cn(vocab, word_idx, question_id_counter, lesson_id)
            questions_bank.append(q)
            question_id_counter += 1
            
        # 4. Audio
        for idx in range(num_audio):
            word_idx = idx % len(vocab)
            q = generate_audio_question(vocab, word_idx, question_id_counter, lesson_id)
            questions_bank.append(q)
            question_id_counter += 1
            
        # 5. Picture
        for idx in range(num_picture):
            word_idx = idx % len(vocab)
            q = generate_picture_question(vocab, word_idx, question_id_counter, lesson_id)
            questions_bank.append(q)
            question_id_counter += 1
            
        # 6. Fill Blank
        for idx in range(num_fill_blank):
            q = generate_fill_blank(vocab, sentences, idx, question_id_counter, lesson_id)
            questions_bank.append(q)
            question_id_counter += 1
            
        # 7. Dialogue
        for idx in range(num_dialogue):
            q = generate_dialogue_question(vocab, dialogues, idx, question_id_counter, lesson_id)
            questions_bank.append(q)
            question_id_counter += 1
            
        # 8. Drag Match
        for idx in range(num_drag_match):
            q = generate_drag_match(vocab, question_id_counter, lesson_id)
            questions_bank.append(q)
            question_id_counter += 1
            
    # Save questions to JSON
    out_dir = r"d:\STUDY\modules\language_game\database"
    out_path = os.path.join(out_dir, "generated_questions.json")
    
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(questions_bank, f, ensure_ascii=False, indent=2)
        
    print(f"Generated {len(questions_bank)} questions successfully! Saved to {out_path}")
    print(f"Average questions per lesson: {len(questions_bank) / len(lessons)}")

if __name__ == "__main__":
    main()
