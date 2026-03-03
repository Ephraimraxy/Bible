import urllib.request
import json
import ssl

API_KEY = "7uxSJHsw4Ku3hRDJHJS4X"
ctx = ssl.create_default_context()

candidates = [
    ("9879dbb7cfe39e4d-01", "WEB", "World English Bible"),
    ("01b29f4b342acc35-01", "LSV", "Literal Standard Version"),
    ("65eec8e0b60e656b-01", "FBV", "Free Bible Version"),
    ("40072c4a5aba4022-01", "RV", "Revised Version 1885"),
    ("179568874c45066f-01", "DRA", "Douay-Rheims")
]

print("Checking public domain English alternatives...")
for bid, abbr, name in candidates:
    url = f"https://rest.api.bible/v1/bibles/{bid}/books"
    req = urllib.request.Request(url, headers={'api-key': API_KEY})
    try:
        with urllib.request.urlopen(req, context=ctx) as resp:
            data = json.loads(resp.read().decode('utf-8'))['data']
            has_ot = any(b['id'] in ['GEN', 'EXO'] for b in data)
            has_nt = any(b['id'] in ['MAT', 'REV'] for b in data)
            count = len(data)
            status = "FULL (66+)" if (has_ot and has_nt and count >= 66) else f"Incomplete ({count} books)"
            print(f"- {name} ({abbr}): {status}")
    except Exception as e:
        print(f"- {name} ({abbr}): [ERROR] {e}")
