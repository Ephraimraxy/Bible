import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
url = 'https://raw.githubusercontent.com/magna25/amharic-bible-json/master/amharic_bible.json'

try:
    with urllib.request.urlopen(url, context=ctx) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        # Just grab the first chapter of Genesis
        first_chap = data['books'][0]['chapters'][0]
        # Save it to a plain text file for viewing
        with open('amharic_sample.txt', 'w', encoding='utf-8') as f:
            f.write(json.dumps(first_chap, indent=2, ensure_ascii=False))
        print("Sample dumped to amharic_sample.txt")
except Exception as e:
    print(f"Error: {e}")
