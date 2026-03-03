"""
Fetches the complete Amharic Bible from magna25/amharic-bible-json on GitHub
and imports it into bible.db.

Structure: { books: [ { title, abbv, chapters: [ { chapter, title, verses: [str, ...] }, ... ] } ] }
"""
import urllib.request
import json
import sqlite3
import ssl
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except AttributeError:
    pass

DB_PATH = "app/src/main/assets/bible.db"
AMHARIC_URL = "https://raw.githubusercontent.com/magna25/amharic-bible-json/master/amharic_bible.json"
VERSION_ID = "AMH"

ctx = ssl.create_default_context()

def fetch_amharic():
    print(f"Fetching Amharic Bible from GitHub...")
    with urllib.request.urlopen(AMHARIC_URL, context=ctx) as resp:
        data = json.loads(resp.read().decode('utf-8'))
    
    books = data.get('books', [])
    print(f"Found {len(books)} books.")

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM verses WHERE version_id=?", (VERSION_ID,))

    verse_count = 0
    for i, book in enumerate(books):
        book_num = i + 1
        book_name = book.get('title', f"Book {book_num}")
        chapters = book.get('chapters', [])
        book_verses = 0

        for ch_idx, ch_data in enumerate(chapters):
            # Each chapter is a dict: {"chapter": "1", "title": "", "verses": [...]}
            try:
                chapter_num = int(ch_data.get('chapter', ch_idx + 1))
            except (ValueError, TypeError):
                chapter_num = ch_idx + 1  # Fallback to index
            verses_list = ch_data.get('verses', [])

            for v_idx, verse_text in enumerate(verses_list):
                verse_num = v_idx + 1
                if not verse_text or not str(verse_text).strip():
                    continue
                c.execute(
                    "INSERT INTO verses (version_id, book_number, book_name, chapter, verse, text) VALUES (?, ?, ?, ?, ?, ?)",
                    (VERSION_ID, book_num, book_name, chapter_num, verse_num, str(verse_text).strip())
                )
                verse_count += 1
                book_verses += 1

        print(f"  {book_num:2d}/66 {book_name[:30]:30s} -> {book_verses} verses")

    conn.commit()
    conn.close()
    print(f"\nDone! Inserted {verse_count} Amharic verses across {len(books)} books.")

if __name__ == "__main__":
    fetch_amharic()
