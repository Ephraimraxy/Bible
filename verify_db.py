import sqlite3

conn = sqlite3.connect('app/src/main/assets/bible.db')
c = conn.cursor()

# Versions
c.execute('SELECT version_id, COUNT(*) FROM verses GROUP BY version_id')
print("=== Versions ===")
for row in c.fetchall():
    print(f"  {row[0]}: {row[1]} verses")

# KJV Books
c.execute("SELECT DISTINCT book_name FROM verses WHERE version_id='KJV' ORDER BY book_number")
books = [r[0] for r in c.fetchall()]
print(f"\n=== KJV Books ({len(books)} total) ===")
for i, b in enumerate(books):
    c.execute("SELECT MAX(chapter) FROM verses WHERE version_id='KJV' AND book_name=?", (b,))
    ch = c.fetchone()[0]
    print(f"  {i+1}. {b} ({ch} chapters)")

# Sample verse
c.execute("SELECT text FROM verses WHERE version_id='KJV' AND book_name='Genesis' AND chapter=1 AND verse=1")
print(f"\n=== Sample: Genesis 1:1 ===")
print(f"  {c.fetchone()[0]}")

c.execute("SELECT text FROM verses WHERE version_id='KJV' AND book_name='Revelation' AND chapter=22 AND verse=21")
print(f"\n=== Sample: Revelation 22:21 ===")
print(f"  {c.fetchone()[0]}")

conn.close()
