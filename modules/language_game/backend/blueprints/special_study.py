import random
from flask import Blueprint, request, jsonify
from ..models import db, SpecialCategory, SpecialWord
from ..utils import token_required

special_study_bp = Blueprint("special_study", __name__)

def _make_options(correct_text, distractors):
    opts = [{'text': correct_text, 'is_correct': True}]
    seen = {correct_text.lower()}
    for d in distractors:
        if d.lower() not in seen:
            opts.append({'text': d, 'is_correct': False})
            seen.add(d.lower())
        if len(opts) >= 4:
            break
    while len(opts) < 4:
        opts.append({'text': '---', 'is_correct': False})
    random.shuffle(opts)
    return opts

@special_study_bp.route("/special/categories", methods=["GET"])
@token_required
def get_categories():
    categories = SpecialCategory.query.order_by(SpecialCategory.id).all()
    return jsonify([c.to_dict() for c in categories]), 200

@special_study_bp.route("/special/words/<int:category_id>", methods=["GET"])
@token_required
def get_category_words(category_id):
    category = SpecialCategory.query.get(category_id)
    if not category:
        return jsonify({"message": "Category not found"}), 404
    words = SpecialWord.query.filter_by(category_id=category_id).all()
    return jsonify([w.to_dict() for w in words]), 200

@special_study_bp.route("/special/questions/<int:category_id>", methods=["GET"])
@token_required
def get_special_questions(category_id):
    mode = request.args.get("mode", "reading")  # 'listening', 'reading', 'writing'
    category = SpecialCategory.query.get(category_id)
    if not category:
        return jsonify({"message": "Category not found"}), 404
        
    words = SpecialWord.query.filter_by(category_id=category_id).all()
    if not words:
        return jsonify({"message": "No words found in this category"}), 404
        
    # Get general pool of all other words in the system for fallback distractors if needed
    all_words_pool = SpecialWord.query.all()
    all_cn_translations = list(set(w.translation for w in all_words_pool))
    all_indo_words = list(set(w.word for w in all_words_pool))

    questions = []
    
    # We generate up to 10 questions. If there are fewer than 10 words, we can repeat or limit.
    # Let's shuffle and take up to 10 distinct words.
    sampled_words = list(words)
    random.shuffle(sampled_words)
    sampled_words = sampled_words[:10]
    
    for idx, item in enumerate(sampled_words):
        word_val = item.word
        trans_val = item.translation
        
        # Distractor pool specific to this category
        others_in_cat = [w for w in words if w.id != item.id]
        
        if mode == "listening":
            # Listening mode: Plays TTS (sends word as content). Option is Chinese translation.
            distractor_pool = [w.translation for w in others_in_cat]
            if len(distractor_pool) < 3:
                # Add from global pool
                extra_distractors = [t for t in all_cn_translations if t.lower() != trans_val.lower()]
                distractor_pool += random.sample(extra_distractors, 3)
            distractors = random.sample(distractor_pool, min(3, len(distractor_pool)))
            
            q = {
                "id": idx + 1,
                "type": "listening",
                "content": word_val,
                "options": _make_options(trans_val, distractors),
                "correct_answer": trans_val,
                "explanation": f"听力发音：印尼语发音单词是 \"{word_val}\"，意思是 \"{trans_val}\"。"
            }
            questions.append(q)
            
        elif mode == "writing":
            # Writing mode: Display Chinese, user types Indonesian spelling.
            # Writing questions don't require multiple choice options.
            q = {
                "id": idx + 1,
                "type": "writing",
                "content": f"请写出中文含义为 <strong>“{trans_val}”</strong> 对应的印尼语单词：",
                "options": [],
                "correct_answer": word_val,
                "explanation": f"词汇拼写：中文意思为 \"{trans_val}\" 的印尼语单词是 \"{word_val}\"。"
            }
            questions.append(q)
            
        else: # reading mode
            # Reading mode: half are Indo -> Chinese, half are Chinese -> Indo
            is_indo_to_cn = (idx % 2 == 0)
            
            if is_indo_to_cn:
                distractor_pool = [w.translation for w in others_in_cat]
                if len(distractor_pool) < 3:
                    extra_distractors = [t for t in all_cn_translations if t.lower() != trans_val.lower()]
                    distractor_pool += random.sample(extra_distractors, 3)
                distractors = random.sample(distractor_pool, min(3, len(distractor_pool)))
                
                q = {
                    "id": idx + 1,
                    "type": "reading_indo_to_cn",
                    "content": f"单词 <strong>“{word_val}”</strong> 的中文意思是什么？",
                    "options": _make_options(trans_val, distractors),
                    "correct_answer": trans_val,
                    "explanation": f"印尼语单词 \"{word_val}\" 的中文意思是 \"{trans_val}\"。"
                }
            else:
                distractor_pool = [w.word for w in others_in_cat]
                if len(distractor_pool) < 3:
                    extra_distractors = [w for w in all_indo_words if w.lower() != word_val.lower()]
                    distractor_pool += random.sample(extra_distractors, 3)
                distractors = random.sample(distractor_pool, min(3, len(distractor_pool)))
                
                q = {
                    "id": idx + 1,
                    "type": "reading_cn_to_indo",
                    "content": f"中文 <strong>“{trans_val}”</strong> 对应的印尼语单词是什么？",
                    "options": _make_options(word_val, distractors),
                    "correct_answer": word_val,
                    "explanation": f"中文 \"{trans_val}\" 对应的印尼语是 \"{word_val}\"。"
                }
            questions.append(q)
            
    return jsonify(questions), 200
