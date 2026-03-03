import sqlite3
import sys

# Standard 66-book Canon with Chapter Counts
CANON = [
    ("Genesis", 50), ("Exodus", 40), ("Leviticus", 27), ("Numbers", 36), ("Deuteronomy", 34),
    ("Joshua", 24), ("Judges", 21), ("Ruth", 4), ("1 Samuel", 31), ("2 Samuel", 24),
    ("1 Kings", 22), ("2 Kings", 25), ("1 Chronicles", 29), ("2 Chronicles", 36),
    ("Ezra", 10), ("Nehemiah", 13), ("Esther", 10), ("Job", 42), ("Psalms", 150),
    ("Proverbs", 31), ("Ecclesiastes", 12), ("Song of Solomon", 8), ("Isaiah", 66),
    ("Jeremiah", 52), ("Lamentations", 5), ("Ezekiel", 48), ("Daniel", 12),
    ("Hosea", 14), ("Joel", 3), ("Amos", 9), ("Obadiah", 1), ("Jonah", 4),
    ("Micah", 7), ("Nahum", 3), ("Habakkuk", 3), ("Zephaniah", 3), ("Haggai", 2),
    ("Zechariah", 14), ("Malachi", 4), ("Matthew", 28), ("Mark", 16), ("Luke", 24),
    ("John", 21), ("Acts", 28), ("Romans", 16), ("1 Corinthians", 16), ("2 Corinthians", 13),
    ("Galatians", 6), ("Ephesians", 6), ("Philippians", 4), ("Colossians", 4),
    ("1 Thessalonians", 5), ("2 Thessalonians", 3), ("1 Timothy", 6), ("2 Timothy", 4),
    ("Titus", 3), ("Philemon", 1), ("Hebrews", 13), ("James", 5), ("1 Peter", 5),
    ("2 Peter", 3), ("1 John", 5), ("2 John", 1), ("3 John", 1), ("Jude", 1),
    ("Revelation", 22)
]

DB_PATH = 'app/src/main/assets/bible.db'

def deep_scan():
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except AttributeError:
        pass

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("SELECT version_id, display_name FROM versions")
    versions = c.fetchall()
    
    print("=" * 100)
    print(f"{'VERSION':10s} | {'STATUS':15s} | {'MISSING BOOKS':20s} | {'CHAPTER ERRORS'}")
    print("-" * 100)
    
    is_flawless = True
    
    for vid, name in versions:
        # 1. Total Verse Check
        c.execute("SELECT COUNT(*) FROM verses WHERE version_id=?", (vid,))
        total_verses = c.fetchone()[0]
        
        # 2. Book Completeness Check
        c.execute("SELECT DISTINCT book_number FROM verses WHERE version_id=? ORDER BY book_number", (vid,))
        found_book_nums = {r[0] for r in c.fetchall()}
        missing_books = []
        for i in range(1, 67):
            if i not in found_book_nums:
                missing_books.append(str(i))
        
        # 3. Chapter Depth Check
        chapter_errors = 0
        for b_idx, (b_name, expected_chaps) in enumerate(CANON):
            b_num = b_idx + 1
            c.execute("SELECT MAX(chapter) FROM verses WHERE version_id=? AND book_number=?", (vid, b_num))
            res = c.fetchone()[0]
            actual_chaps = res if res else 0
            
            if actual_chaps != expected_chaps:
                # Special allowance for some versions (like Hausa) that might have variations in chapter counts,
                # but generally we expect 66 books to match.
                chapter_errors += 1
        
        status = "PERFECT" if not missing_books and chapter_errors == 0 else "REVIEW"
        if status == "REVIEW": is_flawless = False
        
        missing_str = ", ".join(missing_books) if missing_books else "None"
        if len(missing_str) > 18: missing_str = missing_str[:15] + "..."
        
        print(f"{vid:10s} | {status:15s} | {missing_str:20s} | {chapter_errors} books with chapter mismatch")

    print("=" * 100)
    if is_flawless:
        print("\n[SUCCESS] Deep scan complete. Every version contains 66 books with standard chapter counts.")
    else:
        print("\n[NOTICE] Some versions have chapter count variations or missing books. Investigating...")
    
    conn.close()

if __name__ == "__main__":
    deep_scan()
