"""
数据修复脚本 —— 修复 parsed_course.json 中的问题：
1. 修复第1-8课（发音课）中印颠倒的词汇数据
2. 清理无效的句子数据（编号/等号/空翻译）
3. 过滤掉非词汇条目（"JAWAB PERTANYAAN"等）
"""
import json
import re
import os

COURSE_PATH = r"d:\STUDY\modules\language_game\database\parsed_course.json"
OUTPUT_PATH = r"d:\STUDY\modules\language_game\database\parsed_course_fixed.json"

# ============================================================
# 第1步：定义发音课的正确词汇映射（indo→cn）
# 第1课 - 发音（一）：元音、子音字母名称
# ============================================================
PRONUNCIATION_FIXES = {
    1: {
        # 元音 & 双元音
        "AI": "双元音",
        "EI": "哎",
        # 子音发音部位（原数据里的 word 是中文说明，translation 是印尼语）
        # 需要修正为 word=印尼语, translation=中文
        "K": "带嗓音",
        "G": "鼻音",
        "NG": "擦音",
        "H": "带嗓音（子音H）",
        "Z": "颤音",
        "R": "边音",
        "L": "半元音",
        "W": "塞擦音",
        "C": "带嗓音（子音C）",
        "J": "带嗓音（子音J）",
        "SY": "Eng 额",
        # 子音字母名称
        "BE": "贝",
        "CE": "这",
        "DE": "的",
        "EF": "额服",
        "GE": "个",
        "HA": "哈",
        "JE": "贼",
        "KA": "噶",
        "EL": "额乐",
        "EM": "额么",
        "EN": "嗯",
        "PE": "贝",
        "QI": "给",
        "ER": "二",
        "ES": "哎思",
        "TE": "得",
        "VE": "飞",
        "WE": "五额",
        "EKS": "哎可思",
        "YE": "也",
        "ZET": "贼特",
        # 简单词汇
        "AC": "空调",
        "antar jemput": "接送",
        "ada": "有",
        "apa": "什么",
        "adalah": "是",
        "apakah": "......吗？",
        "Agustus": "八月",
        "APD": "劳保（防护用品）",
        "air mineral": "矿泉水",
        "apel": "苹果",
        "akhir-akhir ini": "最近",
        "aplikasi": "应用程序",
        "aku": "我",
        "April": "四月",
        "alergi": "过敏",
        "area": "区域",
        "alkohol": "酒",
        "asam": "酸",
        "aman": "安全",
        "asin": "咸",
        "ambil": "拿",
        "asrama": "宿舍",
        "ambil foto": "拍照",
    },
    2: {
        "Apa": "什么",
        "Sana": "那里",
        "Ada": "有",
        "Sini": "这里",
        "Ini": "这（个）",
        "Nama": "名字",
        "Itu": "那（个）",
        "Saya/Aku": "我",
        "Di...": "在",
        "Kamu": "你",
        "atasan": "上司/领导",
        "ambil sampel": "取样",
        "atau": "或者",
        "Anda": "您",
        "awas": "关注，留意",
        "anggur": "葡萄",
        "bagaimana": "怎么样",
        "berdansa": "跳舞",
        "bagasi": "行李",
        "berdarah": "流血",
        "bahan kimia": "化学物",
        "berdiri": "站",
        "bahaya": "危险",
        "berenang": "游泳",
        "baik": "好",
        "berjalan-jalan": "散步",
        "baik hati": "善良",
        "berlangsung": "持续",
        "bakso": "肉丸",
        "berlari": "跑步",
        "bandara": "飞机场",
        "bermain game": "玩游戏",
        "bantu": "帮助",
    },
    3: {
        "Kami": "我们（不含对方）",
        "Maju": "往前",
        "Kita": "咱们（含对方）",
        "Situ": "那儿",
        "Mereka": "他们",
        "Mana": "哪里",
        "Kanan": "右",
        "Kaki": "脚",
        "Kiri": "左",
        "Jalan": "走/马路",
        "bermain": "玩，打",
        "barang": "东西",
        "bermain bola": "打球",
        "barat": "西",
        "bermain permainan": "玩游戏",
        "basah": "湿",
        "bernyanyi": "唱歌",
        "batal": "取消",
        "bersama": "一起",
        "batuk": "咳嗽",
        "bersepeda": "骑自行车",
        "bawa": "带",
        "bersih": "干净",
        "bea cukai": "海关",
        "berwisata": "旅游",
        "begadang": "熬夜",
        "besok": "明天",
        "bekerja": "做工作，干活",
        "betul": "对",
        "belakang": "后面",
        "biliar": "台球",
        "belanja": "购物",
        "bis": "巴士",
    },
    4: {
        "Anda": "您",
        "Barang": "东西",
        "Kalian": "你们",
        "Sudah": "已经",
        "Terima kasih": "谢谢",
        "Siapa": "谁",
        "Sama-sama": "不客气",
        "Bantu": "帮助",
        "Apakah": "......吗？",
        "Milik": "属于",
        "beli": "买",
        "bisa": "会/能",
        "belok": "拐",
        "biskuit": "饼干",
        "belum": "还没有，尚未",
        "bola voli": "排球",
        "benar": "正确",
        "boleh": "可以",
        "berangin": "刮风",
        "botol minuman": "饮料瓶",
        "berani": "勇敢",
        "buah": "水果",
        "berantakan": "乱",
        "buang": "扔",
        "berapa": "几",
        "bulan": "月",
        "berapa lama": "多久",
        "bulu tangkis": "羽毛球",
        "berasal dari": "来自",
        "bumbu": "调料",
        "berawan": "多云",
        "bungkus": "打包",
        "cabai": "辣椒",
    },
    5: {
        "Karena": "因为",
        "Datang": "来",
        "Betul/benar": "对/正确",
        "Pergi": "去",
        "Salah": "错",
        "Baik": "好",
        "Bisa": "会/能",
        "Oke": "好的",
        "Tidak": "不/没",
        "Mau": "要",
        "cuaca": "天气",
        "cepat": "快",
        "cuci piring": "洗碗",
        "daging ayam": "鸡肉",
        "Desember": "十二月",
        "daging babi": "猪肉",
        "deterjen bubuk": "洗衣粉",
        "daging ikan": "鱼肉",
        "deterjen cair": "洗衣液",
        "daging sapi": "牛肉",
        "di": "在",
        "dalam": "里面",
        "diare": "腹泻",
        "dan": "和",
        "dilarang": "禁止",
        "data": "核对",
        "diperbaiki": "（被）维修",
        "diri": "自己",
        "delapan": "八",
        "diskon": "打折",
        "demam": "发烧",
        "dokter": "医生",
    },
    6: {
        "Satu": "一",
        "Tujuh": "七",
        "Dua": "二",
        "Delapan": "八",
        "Tiga": "三",
        "Sembilan": "九",
        "Empat": "四",
        "Sepuluh": "十",
        "Lima": "五",
        "Nol/Kosong": "零",
        "Enam": "六",
        "denda": "罚款",
        "depan": "前面",
        "dua belas": "十二",
        "departemen": "部门",
        "dua puluh": "二十",
        "desain": "设计",
        "duduk": "坐",
        "enak": "好吃",
        "es krim": "冰淇淋",
        "Februari": "二月",
        "fotografi": "摄影",
        "formulir": "单子",
        "gaji": "工资",
        "gedung": "楼栋",
        "garam": "盐",
        "grup": "组，小队",
        "habis": "（卖）完",
        "hilang": "丢",
        "hadir": "出席",
        "hobi": "爱好",
    },
    7: {
        "Sebelas": "十一",
        "puluh ribu": "万",
        "Dua belas": "十二",
        "ratus ribu": "十万",
        "Dua puluh": "二十",
        "juta": "百万",
        "ratus": "百",
        "miliar": "十亿",
        "ribu": "千",
        "triliun": "兆",
        "hambar": "淡",
        "HP": "手机",
        "hanya": "只，仅仅",
        "hujan": "下雨",
        "hari": "日",
        "hujan deras": "下大雨",
        "hari ini": "今天",
        "hujan gerimis": "下细雨",
        "harus": "必须",
        "humoris": "幽默",
        "hemat": "节俭",
        "ikut": "跟随/参与",
        "istirahat": "休息",
        "Indonesia": "印度尼西亚",
        "istirahat siang": "午休",
        "ini": "这（个）",
        "itu": "那（个）",
        "inspeksi": "检查，检视",
        "izin": "请假",
        "isi formulir": "填写表格",
        "jabatan": "职位",
        "jika": "如果",
        "Jakarta": "雅加达",
    },
    8: {
        "juga": "也",
        "jalan": "走/马路",
        "jujur": "诚实",
        "jam": "小时",
        "Juli": "七月",
        "jangan": "别/不要",
        "Jumat": "星期五",
        "Januari": "一月",
        "Juni": "六月",
        "jeruk": "橘子",
        "juta": "百万",
        "kaki": "脚",
        "kenapa": "为什么",
        "kalau begitu": "那就这样，那么",
        "kentang": "土豆",
        "kalian": "你们",
        "kenyang": "饱",
        "kamar": "房间",
        "keranjang": "篮子",
        "kami": "我们（不含对方）",
        "kereta api": "火车",
        "Kamis": "星期四",
        "kereta cepat": "高铁",
    },
}

# 需要过滤掉的无效词汇模式
NOISE_PATTERNS = [
    r'^JAWAB\s+PERTANYAAN',
    r'^TERJEMAH',
    r'PERTANYAAN',
    r'^A:$',
    r'^B:$',
    r'^印尼标准日期格式',
    r'^子音发音\+中文备注',
    r'^子音表',
    r'^印度尼西亚语双元音',
    r'^\d+[\.\)]',
    r'^[A-Z]\)',
    r'^(=[\s\S]*)?$',
]

def is_noise_word(word):
    """检查是否为无效词汇"""
    for p in NOISE_PATTERNS:
        if re.search(p, word, re.IGNORECASE):
            return True
    return False


def has_meaningful_chinese(text):
    """检查中文是否有意义"""
    if not text:
        return False
    text = text.strip()
    if not text:
        return False
    # 纯编号/等号/短横等
    if re.match(r'^[\d\s\.\)=、\-—]+$', text):
        return False
    # 长度太短
    if len(text) < 2:
        return False
    return True


def fix_pronunciation_lesson_vocab(lesson, fixes):
    """修复发音课的词汇数据"""
    fixed_vocab = []
    for v in lesson.get('vocabulary', []):
        word = v.get('word', '').strip()
        trans = v.get('translation', '').strip()
        
        # 跳过无效噪音词汇
        if is_noise_word(word) or is_noise_word(trans):
            continue
        
        # 检查是否需要修复：如果 word 在 fixes 中，按正确映射修复
        if word in fixes:
            v['translation'] = fixes[word]
            fixed_vocab.append(v)
            continue
        
        # 如果 trans 在 fixes 中（说明原数据是 word/trans 颠倒了）
        if trans in fixes:
            # 交换 word 和 translation
            correct_word = trans
            correct_trans = fixes[trans]
            v['word'] = correct_word
            v['translation'] = correct_trans
            fixed_vocab.append(v)
            continue
        
        # 都不是——检查是否是有效的印尼语词汇
        if not re.search(r'[\u4e00-\u9fff]', word) and has_meaningful_chinese(trans):
            # word 看起来是印尼语，trans 是中文——保留
            fixed_vocab.append(v)
            continue
        
        if has_meaningful_chinese(word) and not re.search(r'[\u4e00-\u9fff]', trans):
            # word 是中文，trans 是印尼语——交换
            v['word'] = trans
            v['translation'] = word
            fixed_vocab.append(v)
            continue
    
    # 去重（基于印尼语词汇去重）
    seen_words = set()
    unique_vocab = []
    for v in fixed_vocab:
        w = v['word'].strip().lower()
        if w not in seen_words:
            seen_words.add(w)
            unique_vocab.append(v)
    
    lesson['vocabulary'] = unique_vocab
    return lesson


def fix_regular_lesson_vocab(lesson):
    """修复普通课的词汇数据"""
    fixed_vocab = []
    seen_words = set()
    
    for v in lesson.get('vocabulary', []):
        word = v.get('word', '').strip()
        trans = v.get('translation', '').strip()
        
        # 跳过噪音
        if is_noise_word(word) or is_noise_word(trans):
            continue
        
        # 确保 word 不含中文（印尼语词汇），trans 是中文
        if re.search(r'[\u4e00-\u9fff]', word) and not re.search(r'[\u4e00-\u9fff]', trans):
            # 交换
            v['word'] = trans
            v['translation'] = word
        elif re.search(r'[\u4e00-\u9fff]', word) and re.search(r'[\u4e00-\u9fff]', trans):
            # 两个都是中文，跳过
            continue
        
        word_clean = v['word'].strip().lower()
        if word_clean not in seen_words and has_meaningful_chinese(v['translation']):
            seen_words.add(word_clean)
            fixed_vocab.append(v)
    
    lesson['vocabulary'] = fixed_vocab
    return lesson


def clean_sentences(lesson):
    """清理无效的句子数据"""
    clean_sents = []
    for s in lesson.get('sentences', []):
        indo = s.get('indonesian', '').strip()
        cn = s.get('chinese', '').strip()
        
        # 确保印尼语和中文都有意义
        if not indo or len(indo) < 3:
            continue
        if not has_meaningful_chinese(cn):
            continue
        if cn in ('=', '==', '-', '--', ''):
            continue
        
        # 确保中文确实是中文（含中文字符）
        if not re.search(r'[\u4e00-\u9fff]', cn):
            # 检查是否是 "2." "3." 这种编号
            if re.match(r'^\d+[\s\.\)]*$', cn):
                continue
            # 如果是印尼语翻译，保留
            if re.search(r'[a-zA-Z]', cn) and len(cn) > 3:
                clean_sents.append(s)
                continue
            continue
        
        clean_sents.append(s)
    
    lesson['sentences'] = clean_sents
    return lesson


def clean_dialogues(lesson):
    """清理对话数据：修复中印尼语顺序颠倒"""
    for d in lesson.get('dialogues', []):
        indo = d.get('indonesian', '').strip()
        cn = d.get('chinese', '').strip()
        
        # 如果 indonesian 是中文，chinese 是印尼语，交换它们
        if re.search(r'[\u4e00-\u9fff]', indo) and not re.search(r'[\u4e00-\u9fff]', cn):
            d['indonesian'] = cn
            d['chinese'] = indo
        
        # 如果 chinese 为空或无效，尝试修复
        cn = d.get('chinese', '').strip()
        if not has_meaningful_chinese(cn):
            # 用 indonesian 中的中文部分
            indo = d.get('indonesian', '')
            cn_match = re.search(r'[\u4e00-\u9fff].*', indo)
            if cn_match:
                d['chinese'] = cn_match.group()
                # 从 indonesian 中移除中文
                d['indonesian'] = re.sub(r'[\u4e00-\u9fff].*', '', indo).strip()
    
    return lesson


def main():
    if not os.path.exists(COURSE_PATH):
        print(f"Error: {COURSE_PATH} not found!")
        return
    
    with open(COURSE_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    lessons = data.get('lessons', [])
    print(f"Loaded {len(lessons)} lessons from {COURSE_PATH}")
    
    stats = {}
    
    for lesson in lessons:
        lid = lesson['id']
        lesson_type = lesson.get('type', 'regular')
        
        before_vocab = len(lesson.get('vocabulary', []))
        before_sents = len(lesson.get('sentences', []))
        
        if lid in PRONUNCIATION_FIXES and lesson_type == 'pronunciation':
            print(f"\n[修复] 发音课第{lid}课 — {lesson['title']}")
            fix_pronunciation_lesson_vocab(lesson, PRONUNCIATION_FIXES[lid])
        else:
            fix_regular_lesson_vocab(lesson)
        
        clean_sentences(lesson)
        clean_dialogues(lesson)
        
        after_vocab = len(lesson.get('vocabulary', []))
        after_sents = len(lesson.get('sentences', []))
        
        stats[lid] = {
            'vocab': (before_vocab, after_vocab),
            'sentences': (before_sents, after_sents),
            'dialogues': len(lesson.get('dialogues', [])),
        }
        
        if before_vocab != after_vocab or before_sents != after_sents:
            print(f"  词汇: {before_vocab} → {after_vocab} (移除了 {before_vocab - after_vocab} 个无效条目)")
            print(f"  句子: {before_sents} → {after_sents} (移除了 {before_sents - after_sents} 个无效条目)")
    
    # 保存修复后的数据
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'='*60}")
    print(f"修复完成！数据已保存至: {OUTPUT_PATH}")
    print(f"{'='*60}")
    
    total_vocab = sum(s['vocab'][1] for s in stats.values())
    total_sents = sum(s['sentences'][1] for s in stats.values())
    total_dials = sum(s['dialogues'] for s in stats.values())
    print(f"\n汇总统计:")
    print(f"  总词汇量: {total_vocab}")
    print(f"  总句子数: {total_sents}")
    print(f"  总对话数: {total_dials}")
    
    # 按课显示
    print(f"\n各课明细:")
    for lid, s in sorted(stats.items()):
        print(f"  第{lid}课 | 词汇:{s['vocab'][1]} | 句子:{s['sentences'][1]} | 对话:{s['dialogues']}")


if __name__ == "__main__":
    main()
