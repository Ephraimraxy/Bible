import urllib.request
import json
import ssl
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except AttributeError:
    pass

ctx = ssl.create_default_context()
url = 'https://raw.githubusercontent.com/magna25/amharic-bible-json/master/amharic_bible.json'

with urllib.request.urlopen(url, context=ctx) as resp:
    data = json.loads(resp.read().decode('utf-8'))
    books = data.get('books', [])
    first_book = books[0]
    chapters = first_book.get('chapters', [])
    first_chap = chapters[0]

    # Write raw structure info
    with open('amharic_debug.txt', 'w', encoding='utf-8') as f:
        f.write(f"Type of chapter: {type(first_chap)}\n")
        f.write(f"Repr of chapter (first 2000 chars):\n")
        f.write(repr(first_chap)[:2000])
        f.write(f"\n\nJSON dump:\n")
        f.write(json.dumps(first_chap, indent=2, ensure_ascii=False)[:3000])

    print("Dumped to amharic_debug.txt")
    print(f"Chapter type: {type(first_chap)}")
    if isinstance(first_chap, dict):
        keys = list(first_chap.keys())
        print(f"Keys (first 10): {keys[:10]}")
        if keys:
            first_val = first_chap[keys[0]]
            print(f"First value type: {type(first_val)}")
            print(f"First value repr: {repr(first_val)[:200]}")
    elif isinstance(first_chap, list):
        print(f"List length: {len(first_chap)}")
        if first_chap:
            print(f"First item type: {type(first_chap[0])}")
            print(f"First item repr: {repr(first_chap[0])[:200]}")
    elif isinstance(first_chap, str):
        print(f"String length: {len(first_chap)}")
        print(f"First 200 chars: {first_chap[:200]}")
