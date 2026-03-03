import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
url = 'https://raw.githubusercontent.com/magna25/amharic-bible-json/master/amharic_bible.json'

try:
    with urllib.request.urlopen(url, context=ctx) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        books = data.get('books', [])
        if len(books) > 0:
            first_book = books[0]
            chapters = first_book.get('chapters', [])
            if len(chapters) > 0:
                first_chapter = chapters[0]
                print(f"Chapter 1 type: {type(first_chapter)}")
                if isinstance(first_chapter, dict):
                    print(f"Chapter 1 keys: {list(first_chapter.keys())}")
                    # Try to find something that looks like verses
                    for key, value in first_chapter.items():
                        print(f"  Key '{key}' type: {type(value)}")
                        if isinstance(value, list):
                            print(f"    Value length: {len(value)}")
                elif isinstance(first_chapter, list):
                    print(f"Chapter 1 is a list of length {len(first_chapter)}")
except Exception as e:
    print(f"Error: {e}")
