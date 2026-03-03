import sqlite3
import sys

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

def inspect_hausa():
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except AttributeError:
        pass

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    print(f"{'Book #':6s} | {'Book Name':25s} | {'Expected':8s} | {'Actual':6s} | {'Diff'}")
    print("-" * 60)
    
    for i, (b_name, expected) in enumerate(CANON):
        b_num = i + 1
        c.execute("SELECT MAX(chapter), COUNT(DISTINCT chapter), book_name FROM verses WHERE version_id='HAU' AND book_number=?", (b_num,))
        max_ch, count_ch, real_name = c.fetchone()
        
        actual = max_ch if max_ch else 0
        diff = actual - expected
        diff_str = f"{diff:+d}" if diff != 0 else "OK"
        
        display_name = (real_name if real_name else "MISSING").encode('ascii', errors='replace').decode('ascii')
        
        print(f"{b_num:6d} | {display_name:25s} | {expected:8d} | {actual:6d} | {diff_str}")

    conn.close()

if __name__ == "__main__":
    inspect_hausa()
