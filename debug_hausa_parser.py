import urllib.request
import urllib.parse
import json
import ssl
import re

def parse_verses_from_content(content):
    verses = []
    if not content: return verses
    parts = re.split(r'<span[^>]*data-number="(\d+)"[^>]*class="v"[^>]*>', content)
    if len(parts) > 1:
        for i in range(1, len(parts), 2):
            if i + 1 < len(parts):
                verse_num = int(parts[i])
                text = parts[i + 1]
                text = re.sub(r'<[^>]+>', ' ', text)
                text = re.sub(r'\s+', ' ', text).strip()
                if text: verses.append((verse_num, text))
    if not verses:
        clean = re.sub(r'<span[^>]*data-number="(\d+)"[^>]*class="v"[^>]*>', r'[[VERSE_\1]]', content)
        clean = re.sub(r'<[^>]+>', ' ', clean)
        clean = re.sub(r'\s+', ' ', clean).strip()
        parts = re.split(r'\[\[VERSE_(\d+)\]\]', clean)
        for i in range(1, len(parts), 2):
            if i + 1 < len(parts):
                verse_num = int(parts[i])
                text = parts[i + 1].strip()
                if text: verses.append((verse_num, text))
    if not verses and content:
        text = re.sub(r'<[^>]+>', ' ', content)
        text = re.sub(r'\s+', ' ', text).strip()
        if text: verses.append((1, text))
    return verses

bible_id = "0ab0c764d56a715d-01" # Hausa
API_KEY = "7uxSJHsw4Ku3hRDJHJS4X"

path = f"/bibles/{bible_id}/chapters/REV.1?content-type=html&include-notes=false&include-titles=false&include-chapter-numbers=false&include-verse-numbers=true&include-verse-spans=true"
safe_path = urllib.parse.quote(path, safe='/?=&')
url = "https://rest.api.bible/v1" + safe_path

ctx = ssl.create_default_context()
req = urllib.request.Request(url, headers={
    'api-key': API_KEY,
    'Accept': 'application/json'
})
response = urllib.request.urlopen(req, context=ctx)
content = json.loads(response.read().decode('utf-8'))['data']['content']

print("--- RAW HTML ---")
print(content[:500].encode('ascii', errors='replace').decode('ascii'))
print("\n--- PARSED VERSES ---")
verses = parse_verses_from_content(content)
print(f"Found {len(verses)} verses")
if verses:
    print(f"Verse 1: {str(verses[0]).encode('ascii', errors='replace').decode('ascii')}")
