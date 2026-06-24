import os
import json
import random
import re

# ─────────────────────────────────────────────────────────────────────────────
# CORE HELPER GENERATORS
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
        trans = v.get('translation', '').strip()
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
    word, translation = item['word'], item['translation']
    others = [w for w in word_list if w['word'] != word]
    distractors = [d['translation'] for d in random.sample(others, min(3, len(others)))]
    return {
        'id': qid, 'lesson_id': lesson_id, 'type': 'vocab_choice',
        'content': '单词"' + word + '"的中文意思是什么？',
        'options': _make_options(translation, distractors),
        'explanation': '印尼语单词"' + word + '"的中文意思是"' + translation + '"。'
    }


def generate_cn_to_indo(word_list, index, qid, lesson_id):
    item = word_list[index % len(word_list)]
    word, translation = item['word'], item['translation']
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
    word, translation = item['word'], item['translation']
    others = [w for w in word_list if w['word'] != word]
    distractors = [d['translation'] for d in random.sample(others, min(3, len(others)))]
    return {
        'id': qid, 'lesson_id': lesson_id, 'type': 'indo_to_cn',
        'content': '选择正确的中文翻译：\n【 ' + word + ' 】',
        'options': _make_options(translation, distractors),
        'explanation': '"' + word + '"翻译成中文是"' + translation + '"。'
    }


def generate_audio_question(word_list, index, qid, lesson_id):
    item = word_list[index % len(word_list)]
    word, translation = item['word'], item['translation']
    others = [w for w in word_list if w['word'] != word]
    distractors = [d['translation'] for d in random.sample(others, min(3, len(others)))]
    return {
        'id': qid, 'lesson_id': lesson_id, 'type': 'audio',
        'content': word,
        'options': _make_options(translation, distractors),
        'explanation': '听音辨义：印尼语发音的单词是"' + word + '"，意思是"' + translation + '"。'
    }


def generate_picture_question(word_list, index, qid, lesson_id):
    item = word_list[index % len(word_list)]
    word, translation = item['word'], item['translation']
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
    clean_sents = [
        (s['indonesian'], s['chinese']) for s in sentences
        if s.get('chinese') and s['chinese'].strip() not in ('=', '')
        and not re.match(r'^\d+[\.\)]', s['chinese'].strip())
        and len(s['chinese'].strip()) > 3
        and re.search(r'[\u4e00-\u9fff]', s['chinese'])
    ]
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
    word, translation = item['word'], item['translation']
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
    if not dialogues:
        return _static_dialogue(qid, lesson_id)
    dial = dialogues[qid % len(dialogues)]
    indo = dial.get('indonesian', '')
    cn = dial.get('chinese', '')
    # skip if cn is noise
    if not cn or not re.search(r'[\u4e00-\u9fff]', cn):
        cn = ''
    g = dial.get('dialogue_group', 1)
    same_group = [d for d in dialogues if d.get('dialogue_group', 1) == g]
    idx_in_group = next((i for i, d in enumerate(same_group) if d['indonesian'] == indo), 0)
    next_idx = (idx_in_group + 1) % len(same_group)
    correct = same_group[next_idx]
    correct_cn = correct.get('chinese', '')
    if not re.search(r'[\u4e00-\u9fff]', correct_cn):
        correct_cn = correct['indonesian']
    correct_text = correct.get('speaker', '') + ': ' + correct['indonesian'] + ' (' + correct_cn + ')'
    others = [d for d in dialogues if d['indonesian'] != correct['indonesian']]
    distractors = []
    for d in others[:3]:
        d_cn = d.get('chinese', d['indonesian'])
        distractors.append(d.get('speaker', '') + ': ' + d['indonesian'] + ' (' + d_cn + ')')
    display_cn = cn if cn else indo
    return {
        'id': qid, 'lesson_id': lesson_id, 'type': 'dialogue',
        'content': '根据对话选择合适的回复：\n【 对方说：' + indo + ' (' + display_cn + ') 】',
        'options': _make_options(correct_text, distractors),
        'explanation': '合适的回复是：' + correct_text
    }


def _static_dialogue(qid, lesson_id):
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
        {
            'content': '根据对话选择最合适的回复：\n【 A: Apakah kamu sudah makan? (你吃饭了吗？) 】',
            'correct': 'B: Sudah, terima kasih. (吃了，谢谢。)',
            'wrong': ['B: Saya tidak tahu. (我不知道。)', 'B: Saya lapar. (我饿了。)', 'B: Mau makan apa? (想吃什么？)'],
            'explanation': '"Sudah"表示"已经"，用来确认已完成某件事。'
        },
        {
            'content': '根据对话选择最合适的回复：\n【 A: Permisi, di mana toilet? (打扰了，洗手间在哪里？) 】',
            'correct': 'B: Di sebelah kanan. (在右边。)',
            'wrong': ['B: Saya tidak di sini. (我不在这里。)', 'B: Ini bukan tempat saya. (这不是我的地方。)', 'B: Tidak tahu. (不知道。)'],
            'explanation': '指引方向用"di sebelah kanan/kiri"（在右边/左边）。'
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
    content_pairs = [{'indo': p['word'], 'cn': p['translation']} for p in pairs]
    return {
        'id': qid, 'lesson_id': lesson_id, 'type': 'drag_match',
        'content': json.dumps(content_pairs, ensure_ascii=False),
        'options': [],
        'explanation': '拖拽匹配：请将印尼语单词与对应的中文含义连线配对。'
    }


# ─────────────────────────────────────────────────────────────────────────────
# LOAD CURATED QUESTIONS FROM JSON DATA FILES
# ─────────────────────────────────────────────────────────────────────────────

def load_curated_data():
    """Load curated question data from JSON files."""
    curated_dir = os.path.join(os.path.dirname(__file__), 'curated')
    curated_map = {}
    if os.path.exists(curated_dir):
        for fname in os.listdir(curated_dir):
            if fname.startswith('lesson_') and fname.endswith('.json'):
                try:
                    lid = int(fname.replace('lesson_', '').replace('.json', ''))
                    with open(os.path.join(curated_dir, fname), 'r', encoding='utf-8') as f:
                        curated_map[lid] = json.load(f)
                except Exception:
                    pass
    return curated_map


# ─────────────────────────────────────────────────────────────────────────────
# GENERATE BALANCED 150-QUESTION SET FOR A LESSON
# ─────────────────────────────────────────────────────────────────────────────

def generate_lesson_questions(lesson, qid_start, curated=None):
    vocab = _filter_vocab(lesson['vocabulary'])
    sentences = lesson.get('sentences', [])
    dialogues = lesson.get('dialogues', [])
    lesson_id = lesson['id']

    if not vocab:
        vocab = lesson['vocabulary']

    questions = []
    qid = qid_start

    # Use curated questions first
    if curated:
        for cq in curated:
            q = dict(cq)
            q['id'] = qid
            q['lesson_id'] = lesson_id
            questions.append(q)
            qid += 1
            if len(questions) >= 60:  # max 60 curated
                break

    curated_count = len(questions)
    need = 150 - curated_count

    # Distribute remaining questions evenly
    n_vocab_choice = need * 22 // 100
    n_cn_to_indo   = need * 18 // 100
    n_indo_to_cn   = need * 18 // 100
    n_audio        = need * 13 // 100
    n_picture      = need *  8 // 100
    n_fill_blank   = need * 10 // 100
    n_dialogue     = need *  6 // 100
    n_drag_match   = need - n_vocab_choice - n_cn_to_indo - n_indo_to_cn - n_audio - n_picture - n_fill_blank - n_dialogue

    for i in range(n_vocab_choice):
        questions.append(generate_vocab_choice(vocab, i, qid, lesson_id))
        qid += 1
    for i in range(n_cn_to_indo):
        questions.append(generate_cn_to_indo(vocab, i, qid, lesson_id))
        qid += 1
    for i in range(n_indo_to_cn):
        questions.append(generate_indo_to_cn(vocab, i, qid, lesson_id))
        qid += 1
    for i in range(n_audio):
        questions.append(generate_audio_question(vocab, i, qid, lesson_id))
        qid += 1
    for i in range(n_picture):
        questions.append(generate_picture_question(vocab, i, qid, lesson_id))
        qid += 1
    for i in range(n_fill_blank):
        questions.append(generate_fill_blank_sentence(sentences, vocab, qid, lesson_id))
        qid += 1
    for i in range(n_dialogue):
        questions.append(generate_dialogue_question(dialogues, vocab, qid, lesson_id))
        qid += 1
    for i in range(max(1, n_drag_match)):
        questions.append(generate_drag_match(vocab, qid, lesson_id))
        qid += 1

    # Pad to 150
    while len(questions) < 150:
        t = qid % 3
        if t == 0:
            questions.append(generate_vocab_choice(vocab, qid % len(vocab), qid, lesson_id))
        elif t == 1:
            questions.append(generate_cn_to_indo(vocab, qid % len(vocab), qid, lesson_id))
        else:
            questions.append(generate_indo_to_cn(vocab, qid % len(vocab), qid, lesson_id))
        qid += 1

    return questions[:150], qid


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    json_path = r"d:\STUDY\modules\language_game\database\parsed_course.json"
    if not os.path.exists(json_path):
        print(f"Error: parsed course JSON not found at {json_path}")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    lessons = data["lessons"]

    # Load curated question data
    curated_map = load_curated_data()
    print(f"Loaded curated data for lessons: {sorted(curated_map.keys())}")

    questions_bank = []
    qid = 1

    print("Generating high-quality question bank...")

    for lesson in lessons:
        lesson_id = lesson["id"]
        curated = curated_map.get(lesson_id)
        lesson_qs, qid = generate_lesson_questions(lesson, qid, curated)
        questions_bank.extend(lesson_qs)
        print(f"  Lesson {lesson_id} ({lesson['title'][:35]}): {len(lesson_qs)} questions")

    out_path = r"d:\STUDY\modules\language_game\database\generated_questions.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(questions_bank, f, ensure_ascii=False, indent=2)

    print(f"\n[OK] Total: {len(questions_bank)} questions saved to {out_path}")
    print(f"[Stats] Average per lesson: {len(questions_bank) / len(lessons):.1f}")

    from collections import Counter
    lesson_counts = Counter(q['lesson_id'] for q in questions_bank)
    for lid, count in sorted(lesson_counts.items()):
        status = "[OK]" if count == 150 else "[WARN]"
        print(f"  {status} Lesson {lid}: {count} questions")


if __name__ == "__main__":
    main()
