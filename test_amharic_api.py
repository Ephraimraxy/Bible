import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
url = 'https://bible-api-kappa.vercel.app/api/v1/verses/amhara/GEN/1'

try:
    print(f"Testing API: {url}")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, context=ctx) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        print(f"Status: {data.get('status')}")
        verses = data.get('data', [])
        print(f"Verse count in GEN 1: {len(verses)}")
        if len(verses) > 0:
            print(f"Sample Verse 1: {verses[0].get('verse')[:100]}")
except Exception as e:
    print(f"Error: {e}")
