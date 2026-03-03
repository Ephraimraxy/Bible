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
            first_book = books[0] # Genesis
            chapters = first_book.get('chapters', [])
            if len(chapters) > 0:
                print(f"Book: {first_book.get('title')}")
                for i in range(min(5, len(chapters))):
                    chapter = chapters[i]
                    print(f"  Chapter {i+1} type: {type(chapter)}")
                    if isinstance(chapter, list):
                        print(f"    Verse count: {len(chapter)}")
                        if len(chapter) > 0:
                            print(f"    First verse sample: {str(chapter[0])[:100]}")
                    elif isinstance(chapter, dict):
                        print(f"    Keys: {list(chapter.keys())}")
except Exception as e:
    print(f"Error: {e}")
