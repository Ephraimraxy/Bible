import urllib.request
import json
import ssl
import sys

ctx = ssl.create_default_context()
url = 'https://raw.githubusercontent.com/magna25/amharic-bible-json/master/amharic_bible.json'

try:
    with urllib.request.urlopen(url, context=ctx) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        books = data.get('books', [])
        if len(books) > 0:
            total_verses = 0
            for b_idx, book in enumerate(books):
                book_verses = 0
                chapters = book.get('chapters', [])
                for ch_idx, chapter in enumerate(chapters):
                    if isinstance(chapter, list):
                        total_verses += len(chapter)
                        book_verses += len(chapter)
                if b_idx < 5: # Only print first 5 books info
                    print(f"Book {b_idx+1}: {len(chapters)} chapters, {book_verses} verses")
            print(f"Total verses in JSON: {total_verses}")
except Exception as e:
    print(f"Error: {e}")
