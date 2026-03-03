import urllib.request
import ssl

ctx = ssl.create_default_context()
urls = [
    "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/am.json",
    "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/et.json",
    "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/amh.json",
    "https://raw.githubusercontent.com/gratis-bible/bible/master/json/am-amh.json",
    "https://raw.githubusercontent.com/sevenrekk/amharic-bible-json/master/amharic_bible_v2.json",
    "https://raw.githubusercontent.com/magna25/amharic-bible-json/master/amharic_bible.json",
    "https://raw.githubusercontent.com/fgeorgatos/Amharic-Bible/master/amharic_bible.json",
]

for url in urls:
    print(f"Checking {url}...")
    req = urllib.request.Request(url, method='HEAD')
    try:
        with urllib.request.urlopen(req, context=ctx) as resp:
            print(f"  [FOUND] Status: {resp.status}, Size: {int(resp.getheader('Content-Length', 0)) / 1024 / 1024:.2f} MB")
    except Exception as e:
        print(f"  [NOT FOUND] {e}")
