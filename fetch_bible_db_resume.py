"""
Fetches Bible translations from API.bible (chapter-level) and GitHub (bulk JSON), 
then builds a single unified bible.db.

Features:
- SMART RESUME: Checks the database and skips books/versions that are already fully downloaded.
- MULTI-KEY SUPPORT: Automatically rotates through API keys if one hits a rate limit or runs out of quota.
"""
import urllib.request
import urllib.error
import urllib.parse
import json
import sqlite3
import os
import time
import ssl
import re
import sys

# Force UTF-8 output on Windows (Pyre doesn't recognize this on all platforms so we ignore the lint)
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace') # type: ignore
except AttributeError:
    pass

DB_NAME = "app/src/main/assets/bible.db"
API_BASE = "https://rest.api.bible/v1"
GITHUB_BASE = "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/"

# ADD YOUR API KEYS HERE. The script will try them in order.
API_KEYS = [
    "uesz2-G0D2gZ0Pnwk2Hgp", # Key 4 (New from User)
    "S82YL-RgYHRZ48BoXmDyD", # Key 3 (Exhausted)
    "7uxSJHsw4Ku3hRDJHJS4X", # Key 2 (Secondary)
]

current_key_idx = 0

# Strict USFM Canonical Mapping
BOOK_MAP = {
    "GEN": 1, "EXO": 2, "LEV": 3, "NUM": 4, "DEU": 5, "JOS": 6, "JDG": 7, "RUT": 8, "1SA": 9, "2SA": 10,
    "1KI": 11, "2KI": 12, "1CH": 13, "2CH": 14, "EZR": 15, "NEH": 16, "EST": 17, "JOB": 18, "PSA": 19, "PRO": 20,
    "ECC": 21, "SNG": 22, "ISA": 23, "JER": 24, "LAM": 25, "EZK": 26, "DAN": 27, "HOS": 28, "JOL": 29, "AMO": 30,
    "OBA": 31, "JON": 32, "MIC": 33, "NAM": 34, "HAB": 35, "ZEP": 36, "HAG": 37, "ZEC": 38, "MAL": 39,
    "MAT": 40, "MRK": 41, "LUK": 42, "JHN": 43, "ACT": 44, "ROM": 45, "1CO": 46, "2CO": 47, "GAL": 48, "EPH": 49,
    "PHP": 50, "COL": 51, "1TH": 52, "2TH": 53, "1TI": 54, "2TI": 55, "TIT": 56, "PHM": 57, "HEB": 58, "JAS": 59,
    "1PE": 60, "2PE": 61, "1JN": 62, "2JN": 63, "3JN": 64, "JUD": 65, "REV": 66
}

# =============== DATABASE ===============

def init_db():
    # DO NOT delete the database if we want to resume!
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

def get_completed_books(conn, version_id):
    """Returns a set of book_numbers that have at least one verse for this version.
    The last downloaded book is presumed partial and omitted so it gets re-downloaded."""
    c = conn.cursor()
    c.execute("SELECT DISTINCT book_number FROM verses WHERE version_id = ?", (version_id,))
    rows = [r[0] for r in c.fetchall()]
    if not rows:
        return set()
    max_book = max(rows)
    # Return all books EXCEPT the maximum one (which was likely interrupted and is partial)
    return set(r for r in rows if r < max_book)

# =============== GITHUB FETCHER (fast bulk) ===============

def fetch_github_bible(conn, filename, version_id, display_name, language, is_english):
    print(f"\n[GitHub] {display_name} ({version_id})")
    
    # Check if this version is already fully downloaded (GitHub Bibles are all or nothing)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM verses WHERE version_id = ?", (version_id,))
    existing_count = c.fetchone()[0]
    if existing_count > 30000: # KJV has 31k, if we have >30k we're probably done
        print(f"  [SKIP] Already fully downloaded ({existing_count} verses)")
        register_version(conn, version_id, display_name, language, is_english)
        return existing_count

    url = GITHUB_BASE + filename
    print(f"  Downloading...")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req)
        data = json.loads(response.read().decode('utf-8-sig'))
    except Exception as e:
        print(f"  [FAIL] Could not download: {e}")
        return 0

    count = 0
    # Delete any partial download for this version before starting fresh
    c.execute("DELETE FROM verses WHERE version_id = ?", (version_id,))
    
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

def api_get(path):
    global current_key_idx
    # URL-encode the path to safely handle special characters in book/chapter IDs, keeping / ? = & unescaped
    safe_path = urllib.parse.quote(path, safe='/?=&')
    url = API_BASE + safe_path
    
    retries = 0
    while retries < len(API_KEYS) * 3: # Try each key 3 times
        api_key = API_KEYS[current_key_idx]
        try:
            req = urllib.request.Request(url, headers={
                'api-key': api_key,
                'Accept': 'application/json',
                'User-Agent': 'Mozilla/5.0'
            })
            ctx = ssl.create_default_context()
            response = urllib.request.urlopen(req, context=ctx, timeout=30)
            return json.loads(response.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            if e.code in [401, 403, 429]: # Unauthorized, Forbidden (Quota), Rate Limit
                print(f"    [!] API Key {current_key_idx+1} hit limit or error ({e.code}). Switching keys...")
                current_key_idx = (current_key_idx + 1) % len(API_KEYS)
                retries += 1
                time.sleep(2) # Backoff before trying new key
            else:
                raise e
        except Exception as e:
            retries += 1
            time.sleep(2)
            if retries >= len(API_KEYS) * 3:
                raise e
    return {}

def parse_verses_from_content(content):
    # Same parsing logic as before
    verses = []
    if not content: return verses
    parts = re.split(r'<span[^>]*data-number="(\d+)"[^>]*class="v"[^>]*>', content)
    if len(parts) > 1:
        for i in range(1, len(parts), 2):
            if i + 1 < len(parts):
                verse_num = int(parts[i])
                text = parts[i + 1]
                text = re.sub(r'<[^>]+>', ' ', text)
                text = re.sub(r'\s+', ' ', text).strip()
                if text: verses.append((verse_num, text))
    if not verses:
        clean = re.sub(r'<span[^>]*data-number="(\d+)"[^>]*class="v"[^>]*>', r'[[VERSE_\1]]', content)
        clean = re.sub(r'<[^>]+>', ' ', clean)
        clean = re.sub(r'\s+', ' ', clean).strip()
        parts = re.split(r'\[\[VERSE_(\d+)\]\]', clean)
        for i in range(1, len(parts), 2):
            if i + 1 < len(parts):
                verse_num = int(parts[i])
                text = parts[i + 1].strip()
                if text: verses.append((verse_num, text))
    if not verses and content:
        text = re.sub(r'<[^>]+>', ' ', content)
        text = re.sub(r'\s+', ' ', text).strip()
        if text: verses.append((1, text))
    return verses

def fetch_api_bible(conn, bible_id, version_id, display_name, language, is_english):
    print(f"\n[API.bible] {display_name} ({version_id})")
    
    # 1. Get books first so we know how many there are (Hausa is NT only = 27 books)
    try:
        books_data = api_get(f"/bibles/{bible_id}/books") or {}
        books = books_data.get("data", []) if books_data else []
    except Exception as e:
        print(f"  [FAIL] Could not fetch book list: {e}")
        return 0

    # Get completed books to resume
    completed_books = get_completed_books(conn, version_id)
    if len(completed_books) >= len(books) and len(books) > 0:
        print("  [SKIP] Bible already fully downloaded.")
        register_version(conn, version_id, display_name, language, is_english)
        return 0 # Already done, no new verses
        
    if len(completed_books) > 0:
        print(f"  [RESUME] Found {len(completed_books)} completed books. Resuming...")

    c = conn.cursor()
    total = 0

    c = conn.cursor()
    total = 0

    for b_idx, book in enumerate(books):
        book_api_id = book.get("id")
        
        # USE CANONICAL MAPPING TO PREVENT MAPPING CORRUPTION
        book_num = BOOK_MAP.get(book_api_id)
        if not book_num:
            # Fallback if book ID is not in our standard map (likely an intro or non-standard book)
            print(f"  [SKIP] Unknown book ID: {book_api_id}")
            continue

        # Ensure book_name can be printed on Windows without UnicodeEncodeError
        book_name = book.get("name", f"Book {book_num}")
        try:
            book_name.encode('cp1252')
            print_name = book_name
        except UnicodeEncodeError:
            print_name = book_name.encode('ascii', errors='replace').decode('ascii')
            
        # book_num is already set via mapping above

        if book_num in completed_books:
            continue

        print(f"  Fetching: {book_num:2d}/66 {print_name:20s}", end="", flush=True)

        # Delete any partial verses for this book before fetching a fresh copy
        c.execute("DELETE FROM verses WHERE version_id = ? AND book_number = ?", (version_id, book_num))
        conn.commit()

        # 2. Get chapters list for this book
        try:
            chaps_data = api_get(f"/bibles/{bible_id}/books/{book_api_id}/chapters") or {}
            chapters = chaps_data.get("data", []) if chaps_data else []
        except Exception as e:
            print(f" -> ERROR fetching chapters for {book_name}: {e}")
            break # Break out of the book loop, the API is probably dead/out of quota

        book_verses = 0
        for chap in chapters:
            try:
                chap_id = chap.get("id")
                chap_num_raw = chap.get("number")

                if chap_num_raw == "intro" or str(chap_id).endswith(".intro"): continue
                try: chap_num = int(chap_num_raw)
                except (ValueError, TypeError): continue

                # 3. Fetch chapter content
                try:
                    chap_content = api_get(f"/bibles/{bible_id}/chapters/{chap_id}?content-type=html&include-notes=false&include-titles=false&include-chapter-numbers=false&include-verse-numbers=true&include-verse-spans=true") or {}
                    content = chap_content.get("data", {}).get("content", "") if chap_content.get("data") else ""
                except Exception as e:
                    time.sleep(0.5)
                    continue

                # 4. Parse verses
                verses = parse_verses_from_content(content)
                for verse_num, text in verses:
                    c.execute("INSERT INTO verses (version_id, book_number, book_name, chapter, verse, text) VALUES (?, ?, ?, ?, ?, ?)",
                              (version_id, book_num, book_name, chap_num, verse_num, text))
                    book_verses += 1
                    total += 1
                time.sleep(0.05)
            except Exception as e:
                safe_err = str(e).encode('ascii', errors='replace').decode('ascii')
                print(f"\n      [!] Chapter parsing crashed: {safe_err}")

        conn.commit()
        print(f" -> Done ({book_verses} verses)")

    register_version(conn, version_id, display_name, language, is_english)
    print(f"  [OK] Downloaded {total} new verses")
    return total

# =============== MAIN ===============

def main():
    if len(API_KEYS) == 0 or API_KEYS[0] == "":
        print("ERROR: No API keys configured.")
        return

    conn = init_db()
    
    # Get current DB count
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM verses")
    start_count = c.fetchone()[0]
    print(f"Starting Database verses: {start_count:,}")

    # ---- GITHUB (fast bulk) ----
    github = [
        ("en_kjv.json",        "KJV", "King James Version",           "English", True),
        ("en_bbe.json",        "BBE", "Bible in Basic English",       "English", True),
        ("de_schlachter.json", "SCH", "Schlachter (German)",          "German",  False),
        ("es_rvr.json",        "RVR", "Reina Valera (Spanish)",      "Spanish", False),
        ("fr_apee.json",       "FRA", "La Bible de l'Epee (French)", "French",  False),
    ]
    for args in github:
        fetch_github_bible(conn, *args)

    # ---- API.BIBLE (chapter-level) ----
    api = [
        ("06125adad2d5898a-01", "ASV", "American Standard Version",     "English", True),
        ("0ab0c764d56a715d-02", "HAU", "Hausa Contemporary Bible",     "Hausa",   False),
        ("a36fc06b086699f1-02", "IGB", "Igbo Contemporary Bible",      "Igbo",    False),
        ("611f8eb23aec8f13-01", "SWA", "Swahili Contemporary Bible",   "Swahili", False),
        ("9879dbb7cfe39e4d-01", "WEB", "World English Bible",           "English", False),
        ("01b29f4b342acc35-01", "LSV", "Literal Standard Version",      "English", False),
        ("65eec8e0b60e656b-01", "FBV", "Free Bible Version",            "English", False),
        ("40072c4a5aba4022-01", "RV",  "Revised Version 1885",          "English", False),
        ("179568874c45066f-01", "DRA", "Douay-Rheims American 1899",    "English", False),
    ]
    for args in api:
        fetch_api_bible(conn, *args)

    # ---- SUMMARY ----
    c.execute("SELECT COUNT(*) FROM verses")
    final_count = c.fetchone()[0]
    
    print(f"\n{'='*60}")
    print(f"NEW VERSES ADDED THIS RUN: {final_count - start_count:,}")
    print(f"TOTAL VESE IN DB:          {final_count:,}")
    print(f"Database: {DB_NAME} ({os.path.getsize(DB_NAME) / (1024*1024):.1f} MB)")
    
    print(f"\n=== Final Verification ===")
    c.execute("""SELECT v.version_id, v.display_name, v.language, COUNT(vs.id)
                 FROM versions v LEFT JOIN verses vs ON v.version_id = vs.version_id
                 GROUP BY v.version_id ORDER BY v.is_english DESC, v.language""")
    for row in c.fetchall():
        print(f"  {row[0]:5s} | {row[1]:30s} | {row[2]:10s} | {row[3]} verses")
    conn.close()

if __name__ == "__main__":
    main()
