"""
Fetches Bible translations from API.bible (chapter-level, FAST) and
GitHub (bulk JSON), then builds a single unified bible.db.

Strategy: fetch each CHAPTER as a single API call, then split paragraphs
into verses using the verse markers in the response.
"""
import urllib.request
import json
import sqlite3
import os
import time
import ssl
import re
import sys

# Force UTF-8 output on Windows
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

DB_NAME = "app/src/main/assets/bible.db"
API_KEY = "RMTurJIneoNdm1SCzKofW"
API_BASE = "https://rest.api.bible/v1"
GITHUB_BASE = "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/"

# =============== DATABASE ===============

def init_db():
    if os.path.exists(DB_NAME):
        try:
            os.remove(DB_NAME)
        except PermissionError:
            # File locked, try renaming the old one
            try:
                os.replace(DB_NAME, DB_NAME + ".old")
            except Exception:
                pass  # Will just overwrite via sqlite
    os.makedirs(os.path.dirname(DB_NAME), exist_ok=True)
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS verses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        version_id TEXT NOT NULL,
        book_number INTEGER NOT NULL,
        book_name TEXT NOT NULL,
        chapter INTEGER NOT NULL,
        verse INTEGER NOT NULL,
        text TEXT NOT NULL,
        is_bookmarked INTEGER DEFAULT 0,
        is_highlighted INTEGER DEFAULT 0
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS versions (
        version_id TEXT PRIMARY KEY,
        display_name TEXT NOT NULL,
        language TEXT NOT NULL,
        is_english INTEGER DEFAULT 0
    )''')
    c.execute('CREATE INDEX IF NOT EXISTS idx_version_book_chapter ON verses (version_id, book_number, chapter)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_search ON verses (version_id, text)')
    conn.commit()
    return conn

def register_version(conn, vid, display_name, language, is_english):
    conn.cursor().execute(
        "INSERT OR REPLACE INTO versions VALUES (?, ?, ?, ?)",
        (vid, display_name, language, 1 if is_english else 0))
    conn.commit()

# =============== GITHUB FETCHER (fast bulk) ===============

def fetch_github_bible(conn, filename, version_id, display_name, language, is_english):
    print(f"\n[GitHub] {display_name} ({version_id})")
    url = GITHUB_BASE + filename
    print(f"  Downloading...")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    response = urllib.request.urlopen(req)
    data = json.loads(response.read().decode('utf-8-sig'))

    c = conn.cursor()
    count = 0
    for b_idx, book_data in enumerate(data):
        book_num = b_idx + 1
        book_name = book_data.get("name", f"Book {book_num}")
        for c_idx, verses in enumerate(book_data.get("chapters", [])):
            chapter_num = c_idx + 1
            for v_idx, text in enumerate(verses):
                verse_num = v_idx + 1
                c.execute("INSERT INTO verses (version_id, book_number, book_name, chapter, verse, text) VALUES (?, ?, ?, ?, ?, ?)",
                          (version_id, book_num, book_name, chapter_num, verse_num, text))
                count += 1
    conn.commit()
    register_version(conn, version_id, display_name, language, is_english)
    print(f"  [OK] {count} verses")
    return count

# =============== API.BIBLE FETCHER (chapter-level) ===============

def api_get(path, retries=3):
    url = API_BASE + path
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={
                'api-key': API_KEY,
                'Accept': 'application/json',
                'User-Agent': 'Mozilla/5.0'
            })
            ctx = ssl.create_default_context()
            response = urllib.request.urlopen(req, context=ctx, timeout=30)
            return json.loads(response.read().decode('utf-8'))
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(1)
            else:
                raise e

def parse_verses_from_content(content):
    """
    API.bible returns chapter content as HTML with verse markers.
    Parse individual verses from the content.
    Returns list of (verse_number, text) tuples.
    """
    verses = []
    if not content:
        return verses

    # API.bible wraps verses in <span> tags with data-number attributes
    # Pattern: <span data-number="1" ...>verse text</span>
    # Or sometimes verse numbers appear as [1], [2] etc.
    
    # First try: split by verse span markers
    # Pattern matches spans with verse numbers
    parts = re.split(r'<span[^>]*data-number="(\d+)"[^>]*class="v"[^>]*>', content)
    
    if len(parts) > 1:
        # parts[0] is before first verse, then alternating: verse_num, text, verse_num, text...
        for i in range(1, len(parts), 2):
            if i + 1 < len(parts):
                verse_num = int(parts[i])
                text = parts[i + 1]
                # Clean HTML tags
                text = re.sub(r'<[^>]+>', ' ', text)
                text = re.sub(r'\s+', ' ', text).strip()
                if text:
                    verses.append((verse_num, text))
    
    # Fallback: try paragraph-based parsing with [num] markers
    if not verses:
        # Remove HTML tags but keep verse number markers
        clean = re.sub(r'<span[^>]*data-number="(\d+)"[^>]*class="v"[^>]*>', r'[[VERSE_\1]]', content)
        clean = re.sub(r'<[^>]+>', ' ', clean)
        clean = re.sub(r'\s+', ' ', clean).strip()
        
        parts = re.split(r'\[\[VERSE_(\d+)\]\]', clean)
        for i in range(1, len(parts), 2):
            if i + 1 < len(parts):
                verse_num = int(parts[i])
                text = parts[i + 1].strip()
                if text:
                    verses.append((verse_num, text))
    
    # Last fallback: treat entire chapter as verse 1
    if not verses and content:
        text = re.sub(r'<[^>]+>', ' ', content)
        text = re.sub(r'\s+', ' ', text).strip()
        if text:
            verses.append((1, text))
    
    return verses

def fetch_api_bible(conn, bible_id, version_id, display_name, language, is_english):
    print(f"\n[API.bible] {display_name} ({version_id})")
    
    # 1. Get books
    books_data = api_get(f"/bibles/{bible_id}/books")
    books = books_data.get("data", [])
    print(f"  Found {len(books)} books")

    c = conn.cursor()
    total = 0

    for b_idx, book in enumerate(books):
        book_api_id = book.get("id")
        book_name = book.get("name", f"Book {b_idx+1}")
        book_num = b_idx + 1

        # 2. Get chapters list for this book
        chaps_data = api_get(f"/bibles/{bible_id}/books/{book_api_id}/chapters")
        chapters = chaps_data.get("data", [])

        for chap in chapters:
            chap_id = chap.get("id")
            chap_num_raw = chap.get("number")

            # Skip intro chapters
            if chap_num_raw == "intro" or str(chap_id).endswith(".intro"):
                continue
            try:
                chap_num = int(chap_num_raw)
            except (ValueError, TypeError):
                continue

            # 3. Fetch full chapter content (ONE request per chapter!)
            try:
                chap_content = api_get(f"/bibles/{bible_id}/chapters/{chap_id}?content-type=html&include-notes=false&include-titles=false&include-chapter-numbers=false&include-verse-numbers=true&include-verse-spans=true")
                content = chap_content.get("data", {}).get("content", "")
            except Exception as e:
                print(f"    WARN: Failed to fetch {chap_id}: {e}")
                time.sleep(0.5)
                continue

            # 4. Parse verses from the chapter content
            verses = parse_verses_from_content(content)

            for verse_num, text in verses:
                c.execute("INSERT INTO verses (version_id, book_number, book_name, chapter, verse, text) VALUES (?, ?, ?, ?, ?, ?)",
                          (version_id, book_num, book_name, chap_num, verse_num, text))
                total += 1

            # Small delay to be polite
            time.sleep(0.05)

        # Commit and show progress per book
        conn.commit()
        print(f"  {book_num:2d}/66 {book_name:20s} ({total} total)")

    register_version(conn, version_id, display_name, language, is_english)
    print(f"  [OK] {total} verses total")
    return total

# =============== MAIN ===============

def main():
    conn = init_db()
    grand = 0

    # ---- GITHUB (fast bulk) ----
    github = [
        ("en_kjv.json",        "KJV", "King James Version",           "English", True),
        ("en_bbe.json",        "BBE", "Bible in Basic English",       "English", True),
        ("de_schlachter.json", "SCH", "Schlachter (German)",          "German",  False),
        ("es_rvr.json",        "RVR", "Reina Valera (Spanish)",      "Spanish", False),
        ("fr_apee.json",       "FRA", "La Bible de l'Epee (French)", "French",  False),
    ]
    for args in github:
        grand += fetch_github_bible(conn, *args)
        time.sleep(0.3)

    # ---- API.BIBLE (chapter-level) ----
    api = [
        ("06125adad2d5898a-01", "ASV", "American Standard Version",     "English", True),
        ("0ab0c764d56a715d-01", "HAU", "Hausa Contemporary Bible",     "Hausa",   False),
        ("a36fc06b086699f1-02", "IGB", "Igbo Contemporary Bible",      "Igbo",    False),
        ("b8d1feac6e94bd74-01", "YOR", "Yoruba Contemporary Bible",    "Yoruba",  False),
    ]
    for args in api:
        grand += fetch_api_bible(conn, *args)

    # ---- SUMMARY ----
    print(f"\n{'='*60}")
    print(f"GRAND TOTAL: {grand} verses")
    print(f"Database: {DB_NAME} ({os.path.getsize(DB_NAME) / (1024*1024):.1f} MB)")
    print(f"\n=== Final Verification ===")
    c = conn.cursor()
    c.execute("""SELECT v.version_id, v.display_name, v.language, COUNT(vs.id)
                 FROM versions v LEFT JOIN verses vs ON v.version_id = vs.version_id
                 GROUP BY v.version_id ORDER BY v.is_english DESC, v.language""")
    for row in c.fetchall():
        print(f"  {row[0]:5s} | {row[1]:40s} | {row[2]:10s} | {row[3]} verses")
    conn.close()

if __name__ == "__main__":
    main()
