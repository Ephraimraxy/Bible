import sqlite3
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except AttributeError:
    pass

DB_PATH = 'app/src/main/assets/bible.db'

def check_order():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    print(f"{'Book #':8s} | {'Swahili Name'}")
    print("-" * 30)
    
    # Check specific milestone books
    milestones = [1, 2, 19, 39, 40, 66]
    for m in milestones:
        c.execute("SELECT DISTINCT book_name FROM verses WHERE version_id='SWA' AND book_number=?", (m,))
        res = c.fetchone()
        name = res[0] if res else "NOT FOUND"
        print(f"{m:8d} | {name}")
        
    conn.close()

if __name__ == "__main__":
    check_order()
