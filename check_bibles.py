import urllib.request
import json

url = "https://getbible.net/index.json"
try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    response = urllib.request.urlopen(req)
    data = json.loads(response.read().decode('utf-8'))
    
    found = {}
    for lang, bibles in data.items():
        if 'yoruba' in lang.lower() or 'hausa' in lang.lower() or 'igbo' in lang.lower() or 'english' in lang.lower():
            for bible in bibles:
                name = bible.get('name', '').lower()
                if 'king james' in name or 'hausa' in name or 'yoruba' in name or 'igbo' in name:
                    found[bible.get('id')] = bible.get('name')
                
    print("Found translations:", found)
except Exception as e:
    print("Error:", e)
