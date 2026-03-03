import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
url = 'https://raw.githubusercontent.com/magna25/amharic-bible-json/master/amharic_bible.json'

try:
    print(f"Fetching {url}...")
    with urllib.request.urlopen(url, context=ctx) as resp:
        content = resp.read()
        print(f"File Size: {len(content) / 1024 / 1024:.2f} MB")
        data = json.loads(content.decode('utf-8'))
        books = data.get('books', [])
        print(f"Total Books: {len(books)}")
        if len(books) > 0:
            total_chapters = 0
            total_verses = 0
            for b in books:
                chaps = b.get('chapters', [])
                total_chapters += len(chaps)
                for c in chaps:
                    total_verses += len(c)
            print(f"Total Chapters: {total_chapters}")
            print(f"Total Verses according to JSON: {total_verses}")
except Exception as e:
    print(f"Error: {e}")
