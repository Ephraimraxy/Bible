import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
url = 'https://raw.githubusercontent.com/magna25/amharic-bible-json/master/amharic_bible.json'

try:
    print(f"Fetching {url}...")
    with urllib.request.urlopen(url, context=ctx) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        print(f"Data type: {type(data)}")
        if isinstance(data, list):
            print(f"List length: {len(data)}")
            if len(data) > 0:
                print("First element structure:")
                first = data[0]
                print(json.dumps(first, indent=2, ensure_ascii=False)[:500])
        elif isinstance(data, dict):
            print(f"Dict keys: {list(data.keys())[:10]}")
            first_key = list(data.keys())[0]
            print(f"First key '{first_key}' content type: {type(data[first_key])}")
except Exception as e:
    print(f"Error: {e}")
