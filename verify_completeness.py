import sqlite3
import sys

# Force UTF-8 output
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except AttributeError:
    pass

DB_PATH = 'app/src/main/assets/bible.db'

def verify():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("SELECT version_id, display_name, language FROM versions")
    versions = c.fetchall()
    
    print(f"{'ID':5s} | {'Name':30s} | {'Lang':10s} | {'Books':5s} | {'Verses':8s} | {'Status'}")
    print("-" * 80)
    
    for vid, name, lang in versions:
        c.execute("SELECT COUNT(DISTINCT book_number) FROM verses WHERE version_id=?", (vid,))
        book_count = c.fetchone()[0]
        
        c.execute("SELECT COUNT(*) FROM verses WHERE version_id=?", (vid,))
        verse_count = c.fetchone()[0]
        
        status = "FULL (66)" if book_count == 66 else f"INCOMPLETE ({book_count}/66)"
        # Note: Some versions might have fewer than 66 books if they are NT only or specialized,
        # but the user requested full versions.
        
        # Hausa currently might be in progress.
        
        print(f"{vid:5s} | {name[:30]:30s} | {lang:10s} | {book_count:5d} | {verse_count:8d} | {status}")
        
    conn.close()

if __name__ == "__main__":
    verify()
