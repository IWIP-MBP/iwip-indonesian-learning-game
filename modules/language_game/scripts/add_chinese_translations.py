import json
import requests
import time

# Common Indonesian to Chinese translations dictionary (manually curated for common words)
INDO_CHINESE_DICT = {
    "saya": "我",
    "anda": "您",
    "kamu": "你",
    "dia": "他/她",
    "kami": "我们",
    "kita": "咱们",
    "mereka": "他们",
    "makan": "吃",
    "minum": "喝",
    "tidur": "睡觉",
    "jalan": "走/路",
    "lari": "跑",
    "duduk": "坐",
    "berdiri": "站立",
    "rumah": "房子",
    "sekolah": "学校",
    "kantor": "办公室",
    "pasar": "市场",
    "toko": "商店",
    "restoran": "餐厅",
    "buku": "书",
    "pensil": "铅笔",
    "meja": "桌子",
    "kursi": "椅子",
    "komputer": "电脑",
    "telepon": "电话",
    "pagi": "早上",
    "siang": "中午",
    "sore": "下午",
    "malam": "晚上",
    "senin": "星期一",
    "selasa": "星期二",
    "rabu": "星期三",
    "ini": "这",
    "itu": "那",
    "sana": "那里",
    "sini": "这里",
    "baik": "好",
    "buruk": "坏",
    "besar": "大",
    "kecil": "小",
    "panjang": "长",
    "pendek": "短",
    "tinggi": "高",
    "rendah": "低",
    "hitam": "黑色",
    "putih": "白色",
    "merah": "红色",
    "biru": "蓝色",
    "hijau": "绿色",
    "kuning": "黄色",
    "coklat": "棕色",
    "satu": "一",
    "dua": "二",
    "tiga": "三",
    "empat": "四",
    "lima": "五",
    "enam": "六",
    "tujuh": "七",
    "delapan": "八",
    "sembilan": "九",
    "sepuluh": "十",
    "beli": "买",
    "jual": "卖",
    "kerja": "工作",
    "belajar": "学习",
    "main": "玩",
    "lihat": "看",
    "dengar": "听",
    "bicara": "说话",
    "senang": "高兴",
    "sedih": "悲伤",
    "marah": "生气",
    "takut": "害怕",
    "lelah": "累",
    "lapar": "饿",
    "haus": "渴",
    "ayah": "父亲",
    "ibu": "母亲",
    "kakak": "哥哥/姐姐",
    "adik": "弟弟/妹妹",
    "anak": "孩子",
    "suami": "丈夫",
    "istri": "妻子",
    "kota": "城市",
    "desa": "村庄",
    "negara": "国家",
    "pulau": "岛屿",
    "laut": "海",
    "gunung": "山",
    "sungai": "河流",
    "mobil": "汽车",
    "bus": "公交车",
    "sepeda": "自行车",
    "pesawat": "飞机",
    "kapal": "船",
    "kereta": "火车",
    "uang": "钱",
    "harga": "价格",
    "murah": "便宜",
    "mahal": "贵",
    "bayar": "支付",
    "tunai": "现金",
    "waktu": "时间",
    "jam": "小时/钟",
    "menit": "分钟",
    "detik": "秒",
    "hari": "天",
    "minggu": "周",
    "bulan": "月",
    "tahun": "年",
    "dokter": "医生",
    "perawat": "护士",
    "guru": "老师",
    "polisi": "警察",
    "tentara": "军人",
    "petani": "农民",
    "air": "水",
    "api": "火",
    "tanah": "土地",
    "udara": "空气",
    "matahari": "太阳",
    "bulan": "月亮",
    "bintang": "星星",
    "hujan": "雨",
    "angin": "风",
    "panas": "热",
    "dingin": "冷",
    "cerah": "晴朗",
    "gelap": "黑暗",
    "cinta": "爱",
    "kasih": "爱/关怀",
    "sayang": "爱/疼爱",
    "benci": "恨",
    "suka": "喜欢",
    "terima": "接受",
    "kasih": "给",
    "maaf": "对不起",
    "permisi": "打扰了",
    "tolong": "请",
    "silakan": "请"
}

def add_chinese_translations(input_path: str, output_path: str):
    """Add Chinese translations to KBBI vocabulary data."""
    with open(input_path, 'r', encoding='utf-8') as f:
        vocabulary = json.load(f)
    
    updated_count = 0
    for item in vocabulary:
        word = item['word'].lower()
        if word in INDO_CHINESE_DICT:
            item['chinese_translation'] = INDO_CHINESE_DICT[word]
            updated_count += 1
        else:
            # Fallback: use Indonesian definition as placeholder
            item['chinese_translation'] = item['translation']
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(vocabulary, f, ensure_ascii=False, indent=2)
    
    print(f"Added Chinese translations to {updated_count}/{len(vocabulary)} words")
    print(f"Saved to: {output_path}")

def main():
    input_path = r"d:\STUDY\modules\language_game\database\kbbi_vocabulary.json"
    output_path = r"d:\STUDY\modules\language_game\database\kbbi_vocabulary_with_chinese.json"
    
    print("Adding Chinese translations to KBBI vocabulary...")
    add_chinese_translations(input_path, output_path)

if __name__ == "__main__":
    main()
