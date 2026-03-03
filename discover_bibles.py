import urllib.request
import json
import ssl

API_KEY = "RMTurJIneoNdm1SCzKofW"
BASE = "https://rest.api.bible/v1"

def api_get(path):
    url = BASE + path
    req = urllib.request.Request(url, headers={
        'api-key': API_KEY,
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0'
    })
    ctx = ssl.create_default_context()
    response = urllib.request.urlopen(req, context=ctx)
    return json.loads(response.read().decode('utf-8'))

data = api_get("/bibles")
bibles = data.get("data", [])

# Search for our targets
keywords = [
    "king james", "nkjv", "new king james",
    "international", "niv",
    "english standard", "esv",
    "new living", "nlt",
    "american standard", "nasb",
    "christian standard", "csb",
    "amplified", "amp",
    "message", "msg",
    "hausa", "yoruba", "igbo",
]

print(f"Total: {len(bibles)} Bibles\n")

for bible in bibles:
    name = (bible.get("name") or "").lower()
    abbr = (bible.get("abbreviation") or "").lower()
    lang_name = bible.get("language", {}).get("name", "").lower()
    bid = bible.get("id", "")
    
    for kw in keywords:
        if kw in name or kw in abbr or kw in lang_name:
            print(f"ID: {bid}")
            print(f"  Name: {bible.get('name')}")
            print(f"  Abbr: {bible.get('abbreviation')}")
            print(f"  Lang: {bible.get('language', {}).get('name')}")
            print()
            break
