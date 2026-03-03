import os
import time
import sqlite3

DB_PATH = "app/src/main/assets/bible.db"

print("Watching bible.db for verse progress (Ctrl+C to stop)...\n")

last_size = 0
last_count = 0

try:
    while True:
        if os.path.exists(DB_PATH):
            size_mb = os.path.getsize(DB_PATH) / (1024 * 1024)
            
            try:
                conn = sqlite3.connect(DB_PATH, timeout=0.1)
                c = conn.cursor()
                c.execute("SELECT COUNT(*) FROM verses")
                count = c.fetchone()[0]
                
                if count != last_count:
                    print(f"\rDatabase Size: {size_mb:.2f} MB | Total Verses: {count:,}          ", end="", flush=True)
                    last_size = size_mb
                    last_count = count
                    
                conn.close()
            except sqlite3.OperationalError:
                # DB might be locked for a split second, ignore
                pass
                
        time.sleep(5)
except KeyboardInterrupt:
    print("\n\nStopped monitoring.")
