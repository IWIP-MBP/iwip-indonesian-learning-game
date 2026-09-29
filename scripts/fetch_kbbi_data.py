import requests
import json
import random
import time
from typing import List, Dict, Optional

# KBBI API endpoints
KBBI_API_BASE = "https://kbbi.raf555.dev/api/v1"

# Common Indonesian words to fetch (beginner to intermediate level)
COMMON_WORDS = [
    "saya", "anda", "kamu", "dia", "kami", "kita", "mereka",
    "makan", "minum", "tidur", "jalan", "lari", "duduk", "berdiri",
    "rumah", "sekolah", "kantor", "pasar", "toko", "restoran",
    "buku", "pensil", "meja", "kursi", "komputer", "telepon",
    "pagi", "siang", "sore", "malam", "senin", "selasa", "rabu",
    "kamu", "dia", "kita", "mereka", "ini", "itu", "sana", "sini",
    "baik", "buruk", "besar", "kecil", "panjang", "pendek", "tinggi", "rendah",
    "hitam", "putih", "merah", "biru", "hijau", "kuning", "coklat",
    "satu", "dua", "tiga", "empat", "lima", "enam", "tujuh", "delapan", "sembilan", "sepuluh",
    "beli", "jual", "kerja", "belajar", "main", "lihat", "dengar", "bicara",
    "senang", "sedih", "marah", "takut", "lelah", "lapar", "haus",
    "ayah", "ibu", "kakak", "adik", "anak", "suami", "istri",
    "kota", "desa", "negara", "pulau", "laut", "gunung", "sungai",
    "mobil", "bus", "sepeda", "pesawat", "kapal", "kereta",
    "uang", "harga", "murah", "mahal", "bayar", "tunai",
    "waktu", "jam", "menit", "detik", "hari", "minggu", "bulan", "tahun",
    "dokter", "perawat", "guru", "polisi", "tentara", "petani",
    "air", "api", "tanah", "udara", "matahari", "bulan", "bintang",
    "hujan", "angin", "panas", "dingin", "cerah", "gelap",
    "cinta", "kasih", "sayang", "benci", "suka", "tidak suka",
    "terima", "kasih", "maaf", "permisi", "tolong", "silakan"
]

def fetch_word_data(word: str) -> Optional[Dict]:
    """Fetch word data from KBBI API."""
    try:
        url = f"{KBBI_API_BASE}/entry/{word}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"  Status {response.status_code} for '{word}'")
        return None
    except Exception as e:
        print(f"Error fetching '{word}': {e}")
        return None

def extract_meanings(data: Dict) -> List[str]:
    """Extract meanings from KBBI API response."""
    meanings = []
    
    # Handle KBBI API structure: entries[].definitions[].definition
    if 'entries' in data and isinstance(data['entries'], list):
        for entry in data['entries']:
            if 'definitions' in entry and isinstance(entry['definitions'], list):
                for definition in entry['definitions']:
                    if 'definition' in definition:
                        meanings.append(definition['definition'])
    
    # Fallback for other structures
    elif 'data' in data and isinstance(data['data'], list):
        for item in data['data']:
            if 'meanings' in item:
                for meaning in item['meanings']:
                    if 'definition' in meaning:
                        meanings.append(meaning['definition'])
            elif 'meaning' in item:
                meanings.append(item['meaning'])
            elif 'makna' in item:
                if isinstance(item['makna'], list):
                    for m in item['makna']:
                        if isinstance(m, dict) and 'definisi' in m:
                            meanings.append(m['definisi'])
                        elif isinstance(m, str):
                            meanings.append(m)
                else:
                    meanings.append(str(item['makna']))
    elif 'meanings' in data:
        for meaning in data['meanings']:
            if 'definition' in meaning:
                meanings.append(meaning['definition'])
    elif 'meaning' in data:
        meanings.append(data['meaning'])
    elif 'makna' in data:
        if isinstance(data['makna'], list):
            for m in data['makna']:
                if isinstance(m, dict) and 'definisi' in m:
                    meanings.append(m['definisi'])
                elif isinstance(m, str):
                    meanings.append(m)
        else:
            meanings.append(str(data['makna']))
    
    return meanings

def extract_examples(data: Dict) -> List[str]:
    """Extract example sentences from KBBI API response."""
    examples = []
    
    # Handle KBBI API structure: entries[].definitions[].usageExamples
    if 'entries' in data and isinstance(data['entries'], list):
        for entry in data['entries']:
            if 'definitions' in entry and isinstance(entry['definitions'], list):
                for definition in entry['definitions']:
                    if 'usageExamples' in definition and isinstance(definition['usageExamples'], list):
                        examples.extend(definition['usageExamples'])
    
    # Fallback for other structures
    elif 'meanings' in data:
        for meaning in data['meanings']:
            if 'examples' in meaning:
                examples.extend(meaning['examples'])
    elif 'data' in data and isinstance(data['data'], list):
        for item in data['data']:
            if 'meanings' in item:
                for meaning in item['meanings']:
                    if 'examples' in meaning:
                        examples.extend(meaning['examples'])
    
    return examples

def fetch_vocabulary_data(words: List[str]) -> List[Dict]:
    """Fetch vocabulary data for a list of words."""
    vocabulary = []
    total = len(words)
    
    for i, word in enumerate(words):
        print(f"Fetching {i+1}/{total}: {word}")
        data = fetch_word_data(word)
        
        if data:
            meanings = extract_meanings(data)
            examples = extract_examples(data)
            
            # Simplify meaning to first definition if available
            primary_meaning = meanings[0] if meanings else word
            # Clean up meaning text
            primary_meaning = primary_meaning.split('\n')[0].strip()
            
            vocab_entry = {
                'word': word,
                'translation': primary_meaning,
                'phonetic': data.get('pronunciation', None),
                'meanings': meanings,
                'examples': examples
            }
            vocabulary.append(vocab_entry)
        
        # Rate limiting
        time.sleep(0.5)
    
    return vocabulary

def save_vocabulary_data(vocabulary: List[Dict], output_path: str):
    """Save vocabulary data to JSON file."""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(vocabulary, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(vocabulary)} vocabulary entries to {output_path}")

def main():
    print("Fetching Indonesian vocabulary from KBBI API...")
    
    # Fetch data for common words
    vocabulary = fetch_vocabulary_data(COMMON_WORDS)
    
    # Save to file
    output_path = r"d:\STUDY\modules\language_game\database\kbbi_vocabulary.json"
    save_vocabulary_data(vocabulary, output_path)
    
    print(f"\nSuccessfully fetched {len(vocabulary)} words from KBBI")
    print("Data saved to:", output_path)

if __name__ == "__main__":
    main()
