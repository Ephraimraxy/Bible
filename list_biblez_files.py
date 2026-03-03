import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
url = 'https://api.github.com/repos/BibleZ/biblez-translations/contents/'

try:
    print(f"Fetching file list from {url}...")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, context=ctx) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        files = [item['name'] for item in data]
        print(f"Total files: {len(files)}")
        for f in sorted(files):
            if 'amh' in f.lower() or 'am' in f.lower():
                print(f"Possible match: {f}")
except Exception as e:
    print(f"Error: {e}")
