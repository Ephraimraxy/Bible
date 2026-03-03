import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
url = 'https://raw.githubusercontent.com/magna25/amharic-bible-json/master/amharic_bible.json'

try:
    print(f"Fetching {url}...")
    with urllib.request.urlopen(url, context=ctx) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        books = data.get('books', [])
        print(f"Number of books: {len(books)}")
        if len(books) > 0:
            first_book = books[0]
            print(f"First book keys: {list(first_book.keys())}")
            print(f"First book name: {first_book.get('title')}")
            chapters = first_book.get('chapters', [])
            print(f"Number of chapters in first book: {len(chapters)}")
            if len(chapters) > 0:
                first_chapter = chapters[0]
                print(f"First chapter type: {type(first_chapter)}")
                if isinstance(first_chapter, list):
                     print(f"First chapter verses: {len(first_chapter)}")
                     if len(first_chapter) > 0:
                         print(f"First verse sample: {first_chapter[0][:100]}")
except Exception as e:
    print(f"Error: {e}")
