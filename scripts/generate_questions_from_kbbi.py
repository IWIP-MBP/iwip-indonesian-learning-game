import os
import json
import random
import re

# ─────────────────────────────────────────────────────────────────────────────
# CORE HELPER GENERATORS (adapted from generate_questions.py)
# ─────────────────────────────────────────────────────────────────────────────

def _filter_vocab(vocab):
    noise_patterns = [
        r'^\d+[\.\)]',
        r'^JAWAB',
        r'^TERJEMAH',
        r'PERTANYAAN',
        r'^A:$',
        r'^B:$',
    ]
    clean = []
    for v in vocab:
        word = v.get('word', '').strip()
        trans = v.get('chinese_translation', v.get('translation', '')).strip()
        if not word or not trans:
            continue
        if any(re.search(p, word, re.IGNORECASE) for p in noise_patterns):
            continue
        if trans in ('=', '==', '-', '--', ''):
            continue
        if len(trans) < 1 or len(word) < 1:
            continue
        clean.append(v)
    return clean


def _make_options(correct_text, distractors, shuffle=True):
    opts = [{'text': correct_text, 'is_correct': True}]
    seen = {correct_text}
    for d in distractors:
        if d not in seen:
            opts.append({'text': d, 'is_correct': False})
            seen.add(d)
        if len(opts) >= 4:
            break
    while len(opts) < 4:
        opts.append({'text': '---', 'is_correct': False})
    if shuffle:
        random.shuffle(opts)
    return opts


def generate_vocab_choice(word_list, index, qid, lesson_id):
    item = word_list[index % len(word_list)]
    word = item['word']
    translation = item.get('chinese_translation', item.get('translation', ''))
    others = [w for w in word_list if w['word'] != word]
    distractors = [d.get('chinese_translation', d.get('translation', '')) for d in random.sample(others, min(3, len(others)))]
    return {
        'id': qid, 'lesson_id': lesson_id, 'type': 'vocab_choice',
        'content': '单词"' + word + '"的中文意思是什么？',
        'options': _make_options(translation, distractors),
        'explanation': '印尼语单词"' + word + '"的中文意思是"' + translation + '"。'
    }


def generate_cn_to_indo(word_list, index, qid, lesson_id):
    item = word_list[index % len(word_list)]
    word = item['word']
    translation = item.get('chinese_translation', item.get('translation', ''))
    others = [w for w in word_list if w['word'] != word]
    distractors = [d['word'] for d in random.sample(others, min(3, len(others)))]
    return {
        'id': qid, 'lesson_id': lesson_id, 'type': 'cn_to_indo',
        'content': '中文"' + translation + '"对应的印尼语单词是什么？',
        'options': _make_options(word, distractors),
        'explanation': '中文"' + translation + '"对应的印尼语是"' + word + '"。'
    }


def generate_indo_to_cn(word_list, index, qid, lesson_id):
    item = word_list[index % len(word_list)]
    word = item['word']
    translation = item.get('chinese_translation', item.get('translation', ''))
    others = [w for w in word_list if w['word'] != word]
    distractors = [d.get('chinese_translation', d.get('translation', '')) for d in random.sample(others, min(3, len(others)))]
    return {
        'id': qid, 'lesson_id': lesson_id, 'type': 'indo_to_cn',
        'content': '选择正确的中文翻译：\n【 ' + word + ' 】',
        'options': _make_options(translation, distractors),
        'explanation': '"' + word + '"翻译成中文是"' + translation + '"。'
    }


def generate_audio_question(word_list, index, qid, lesson_id):
    item = word_list[index % len(word_list)]
    word = item['word']
    translation = item.get('chinese_translation', item.get('translation', ''))
    others = [w for w in word_list if w['word'] != word]
    distractors = [d.get('chinese_translation', d.get('translation', '')) for d in random.sample(others, min(3, len(others)))]
    return {
        'id': qid, 'lesson_id': lesson_id, 'type': 'audio',
        'content': word,
        'options': _make_options(translation, distractors),
        'explanation': '听音辨义：印尼语发音的单词是"' + word + '"，意思是"' + translation + '"。'
    }


def generate_picture_question(word_list, index, qid, lesson_id):
    item = word_list[index % len(word_list)]
    word = item['word']
    translation = item.get('chinese_translation', item.get('translation', ''))
    others = [w for w in word_list if w['word'] != word]
    distractors = [d['word'] for d in random.sample(others, min(3, len(others)))]
    img_name = word.lower().replace(' ', '_').replace('/', '_')
    return {
        'id': qid, 'lesson_id': lesson_id, 'type': 'picture',
        'content': '请选择与图片相对应的印尼语单词：',
        'image_path': '/assets/images/quiz/' + img_name + '.png',
        'options': _make_options(word, distractors),
        'explanation': '图片展示的是"' + translation + '"，对应的印尼语单词是"' + word + '"。'
    }


def generate_fill_blank_sentence(sentences, vocab, qid, lesson_id):
    # Generate fill blank from example sentences if available
    clean_sents = []
    for item in vocab:
        if 'examples' in item and item['examples']:
            for example in item['examples']:
                if example and example.strip() and len(example.strip()) > 3:
                    clean_sents.append((example, item.get('chinese_translation', item.get('translation', ''))))
    
    if not clean_sents:
        return _fill_blank_word_spelling(vocab, qid, lesson_id)

    idx = qid % len(clean_sents)
    indo, cn = clean_sents[idx]
    words = re.findall(r'\b[a-zA-Z\-]+\b', indo)
    masked_word = None
    for w in words:
        if any(v['word'].lower() == w.lower() for v in vocab):
            masked_word = w
            break
    if not masked_word and words:
        candidates = [w for w in words if len(w) > 2]
        masked_word = random.choice(candidates) if candidates else words[0]
    if not masked_word:
        return _fill_blank_word_spelling(vocab, qid, lesson_id)

    masked_indo = re.sub(r'\b' + re.escape(masked_word) + r'\b', '_______', indo, count=1)
    distractor_words = [v['word'] for v in vocab if v['word'].lower() != masked_word.lower()]
    if len(distractor_words) < 3:
        distractor_words += ['saya', 'itu', 'ini', 'di', 'ada', 'dan']
    distractors = random.sample(distractor_words, min(3, len(distractor_words)))
    return {
        'id': qid, 'lesson_id': lesson_id, 'type': 'fill_blank',
        'content': '补全句子：\n' + masked_indo + '\n（中文释义：' + cn + '）',
        'options': _make_options(masked_word, distractors),
        'explanation': '本句意为"' + cn + '"。需要填入"' + masked_word + '"。完整句子：' + indo
    }


def _fill_blank_word_spelling(vocab, qid, lesson_id):
    item = vocab[qid % len(vocab)]
    word = item['word']
    translation = item.get('chinese_translation', item.get('translation', ''))
    if len(word) < 3:
        return {
            'id': qid, 'lesson_id': lesson_id, 'type': 'fill_blank',
            'content': 'Saya ___ sini. （我在这里。）',
            'options': _make_options('di', ['ke', 'dari', 'ini']),
            'explanation': '表达在某处使用介词"di"。正确句子是"Saya di sini."'
        }
    mask_idx = random.randint(1, len(word) - 2)
    masked_char = word[mask_idx]
    masked_word_str = word[:mask_idx] + '_' + word[mask_idx+1:]
    vowels = ['a', 'i', 'u', 'e', 'o']
    consonants = ['n', 'r', 'k', 't', 's', 'm', 'l']
    pool = vowels if masked_char.lower() in vowels else consonants
    distractors = [c for c in pool if c != masked_char.lower()][:3]
    return {
        'id': qid, 'lesson_id': lesson_id, 'type': 'fill_blank',
        'content': '请补全单词拼写：\n【 ' + masked_word_str + ' 】\n（中文释义：' + translation + '）',
        'options': _make_options(masked_char, distractors),
        'explanation': '印尼语单词"' + word + '"意为"' + translation + '"，缺失的字母是"' + masked_char + '"。'
    }


def generate_dialogue_question(dialogues, vocab, qid, lesson_id):
    # Static dialogue questions since we don't have dialogue data from KBBI
    templates = [
        {
            'content': '根据对话选择最合适的回复：\n【 A: Selamat pagi! (早上好！) 】',
            'correct': 'B: Selamat pagi! (早上好！)',
            'wrong': ['B: Selamat malam! (晚上好！)', 'B: Terima kasih. (谢谢。)', 'B: Nama saya Tata. (我叫Tata。)'],
            'explanation': '问候"早上好"应该回答"Selamat pagi!"'
        },
        {
            'content': '根据对话选择最合适的回复：\n【 A: Terima kasih! (谢谢！) 】',
            'correct': 'B: Sama-sama. (不客气。)',
            'wrong': ['B: Maaf. (对不起。)', 'B: Permisi. (打扰了。)', 'B: Tidak apa-apa. (没关系。)'],
            'explanation': '回应感谢应说"Sama-sama."（不客气）'
        },
        {
            'content': '根据对话选择最合适的回复：\n【 A: Siapa nama kamu? (你叫什么名字？) 】',
            'correct': 'B: Nama saya Andi. (我叫Andi。)',
            'wrong': ['B: Saya dari Jakarta. (我来自雅加达。)', 'B: Saya dua puluh tahun. (我20岁。)', 'B: Saya senang. (我很高兴。)'],
            'explanation': '被问名字时回答"Nama saya ___."'
        },
        {
            'content': '根据对话选择最合适的回复：\n【 A: Kamu berasal dari mana? (你来自哪里？) 】',
            'correct': 'B: Saya berasal dari Tiongkok. (我来自中国。)',
            'wrong': ['B: Saya baik-baik saja. (我很好。)', 'B: Umur saya 25 tahun. (我25岁。)', 'B: Hobi saya membaca. (我的爱好是看书。)'],
            'explanation': '被问籍贯时回答"Saya berasal dari ___."'
        },
        {
            'content': '根据对话选择最合适的回复：\n【 A: Apa kabar? (你好吗？) 】',
            'correct': 'B: Baik, terima kasih. (很好，谢谢。)',
            'wrong': ['B: Tidak bisa. (不能。)', 'B: Saya lapar. (我饿了。)', 'B: Maaf, saya tidak tahu. (对不起，我不知道。)'],
            'explanation': '"Apa kabar?"是问候语，回答"Baik, terima kasih."'
        },
    ]
    t = templates[qid % len(templates)]
    return {
        'id': qid, 'lesson_id': lesson_id, 'type': 'dialogue',
        'content': t['content'],
        'options': _make_options(t['correct'], t['wrong']),
        'explanation': t['explanation']
    }


def generate_drag_match(word_list, qid, lesson_id):
    pairs = random.sample(word_list, min(4, len(word_list)))
    content_pairs = [{'indo': p['word'], 'cn': p.get('chinese_translation', p.get('translation', ''))} for p in pairs]
    return {
        'id': qid, 'lesson_id': lesson_id, 'type': 'drag_match',
        'content': json.dumps(content_pairs, ensure_ascii=False),
        'options': [],
        'explanation': '拖拽匹配：请将印尼语单词与对应的中文含义连线配对。'
    }


# ─────────────────────────────────────────────────────────────────────────────
# GENERATE QUESTIONS FROM KBBI DATA
# ─────────────────────────────────────────────────────────────────────────────

def generate_questions_from_kbbi(vocab_path, output_path, total_questions=3150):
    """Generate questions from KBBI vocabulary data."""
    
    with open(vocab_path, 'r', encoding='utf-8') as f:
        vocabulary = json.load(f)
    
    vocab = _filter_vocab(vocabulary)
    print(f"Filtered vocabulary: {len(vocab)} words")
    
    if not vocab:
        print("Error: No valid vocabulary found")
        return
    
    questions_bank = []
    qid = 1
    lesson_id = 1  # All questions from KBBI will be lesson 1 for now
    
    # Distribute question types
    n_vocab_choice = total_questions * 25 // 100
    n_cn_to_indo   = total_questions * 20 // 100
    n_indo_to_cn   = total_questions * 20 // 100
    n_audio        = total_questions * 15 // 100
    n_picture      = total_questions * 10 // 100
    n_fill_blank   = total_questions *  5 // 100
    n_dialogue     = total_questions *  3 // 100
    n_drag_match   = total_questions - n_vocab_choice - n_cn_to_indo - n_indo_to_cn - n_audio - n_picture - n_fill_blank - n_dialogue
    
    print(f"Generating {total_questions} questions...")
    print(f"  vocab_choice: {n_vocab_choice}")
    print(f"  cn_to_indo: {n_cn_to_indo}")
    print(f"  indo_to_cn: {n_indo_to_cn}")
    print(f"  audio: {n_audio}")
    print(f"  picture: {n_picture}")
    print(f"  fill_blank: {n_fill_blank}")
    print(f"  dialogue: {n_dialogue}")
    print(f"  drag_match: {n_drag_match}")
    
    for i in range(n_vocab_choice):
        questions_bank.append(generate_vocab_choice(vocab, i, qid, lesson_id))
        qid += 1
    for i in range(n_cn_to_indo):
        questions_bank.append(generate_cn_to_indo(vocab, i, qid, lesson_id))
        qid += 1
    for i in range(n_indo_to_cn):
        questions_bank.append(generate_indo_to_cn(vocab, i, qid, lesson_id))
        qid += 1
    for i in range(n_audio):
        questions_bank.append(generate_audio_question(vocab, i, qid, lesson_id))
        qid += 1
    for i in range(n_picture):
        questions_bank.append(generate_picture_question(vocab, i, qid, lesson_id))
        qid += 1
    for i in range(n_fill_blank):
        questions_bank.append(generate_fill_blank_sentence([], vocab, qid, lesson_id))
        qid += 1
    for i in range(n_dialogue):
        questions_bank.append(generate_dialogue_question([], vocab, qid, lesson_id))
        qid += 1
    for i in range(max(1, n_drag_match)):
        questions_bank.append(generate_drag_match(vocab, qid, lesson_id))
        qid += 1
    
    # Pad to total_questions
    while len(questions_bank) < total_questions:
        t = qid % 3
        if t == 0:
            questions_bank.append(generate_vocab_choice(vocab, qid % len(vocab), qid, lesson_id))
        elif t == 1:
            questions_bank.append(generate_cn_to_indo(vocab, qid % len(vocab), qid, lesson_id))
        else:
            questions_bank.append(generate_indo_to_cn(vocab, qid % len(vocab), qid, lesson_id))
        qid += 1
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(questions_bank[:total_questions], f, ensure_ascii=False, indent=2)
    
    print(f"\n[OK] Total: {len(questions_bank[:total_questions])} questions saved to {output_path}")


def main():
    vocab_path = r"d:\STUDY\modules\language_game\database\kbbi_vocabulary_with_chinese.json"
    output_path = r"d:\STUDY\modules\language_game\database\generated_questions.json"
    
    print("Generating questions from KBBI online data...")
    generate_questions_from_kbbi(vocab_path, output_path, total_questions=3150)


if __name__ == "__main__":
    main()
