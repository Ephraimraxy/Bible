import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
url = 'https://raw.githubusercontent.com/magna25/amharic-bible-json/master/amharic_bible.json'

try:
    with urllib.request.urlopen(url, context=ctx) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        books = data.get('books', [])
        for i, b in enumerate(books):
            print(f"{i+1}: {b.get('abbv')} ({b.get('title')})")
except Exception as e:
    print(f"Error: {e}")
