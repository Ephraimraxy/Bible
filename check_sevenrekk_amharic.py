import urllib.request
import ssl

ctx = ssl.create_default_context()
url = 'https://raw.githubusercontent.com/sevenrekk/amharic-bible-json/master/amharic_bible_v2.json'

try:
    print(f"Checking {url}...")
    req = urllib.request.Request(url, method='HEAD')
    with urllib.request.urlopen(req, context=ctx) as resp:
        print(f"Status: {resp.status}")
        size = int(resp.getheader('Content-Length', 0))
        print(f"Size: {size / 1024 / 1024:.2f} MB")
except Exception as e:
    print(f"Error: {e}")
