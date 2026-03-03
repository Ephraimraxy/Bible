import sqlite3
DB_PATH = 'app/src/main/assets/bible.db'
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.execute("SELECT version_id, count(*), count(distinct book_number) FROM verses GROUP BY version_id")
rows = c.fetchall()
print(f"{'ID':8s} | {'Verses':8s} | {'Books':8s}")
print("-" * 30)
for r in rows:
    print(f"{r[0]:8s} | {r[1]:8d} | {r[2]:8d}")
conn.close()
