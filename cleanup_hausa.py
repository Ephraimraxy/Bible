import sqlite3
import os

DB_PATH = 'app/src/main/assets/bible.db'

def cleanup():
    if not os.path.exists(DB_PATH):
        print("Database not found.")
        return
        
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    print("Deleting Hausa verses...")
    c.execute("DELETE FROM verses WHERE version_id='HAU'")
    print(f"Removed {c.rowcount} verses.")
    
    conn.commit()
    conn.close()
    print("Hausa data cleared successfully.")

if __name__ == "__main__":
    cleanup()
