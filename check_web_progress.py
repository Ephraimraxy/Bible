import sqlite3
DB_PATH = 'app/src/main/assets/bible.db'
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.execute("SELECT MAX(book_number) FROM verses WHERE version_id='WEB'")
print(f"WEB max book: {c.fetchone()[0]}")
c.execute("SELECT COUNT(*) FROM verses WHERE version_id='WEB'")
print(f"WEB total verses: {c.fetchone()[0]}")
conn.close()
