import urllib.request
import json
import ssl
import sys

# Force UTF-8 output
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except AttributeError:
    pass

API_KEY = "7uxSJHsw4Ku3hRDJHJS4X"

def search_versions(query=None, language=None):
    url = "https://rest.api.bible/v1/bibles"
    if language:
        url += f"?language={language}"
    
    req = urllib.request.Request(url, headers={'api-key': API_KEY})
    ctx = ssl.create_default_context()
    
    try:
        with urllib.request.urlopen(req, context=ctx) as response:
            data = json.loads(response.read().decode('utf-8'))['data']
            results = []
            for b in data:
                if query:
                    if query.lower() in b['name'].lower() or query.lower() in b['abbreviation'].lower():
                        results.append(b)
                else:
                    results.append(b)
            return results
    except Exception as e:
        print(f"Error: {e}")
        return []

requested_full_names = [
    "New International Version",
    "English Standard Version",
    "New King James Version",
    "New Living Translation",
    "The Message",
    "Good News Translation",
    "Contemporary English Version",
    "New American Standard Bible",
    "Amplified Bible"
]

print("=== Broader Search Results ===")

for q in requested_full_names:
    res = search_versions(query=q)
    if res:
        for b in res:
            print(f"[FOUND] {q} -> {b['name']} ({b['id']})")
    else:
        print(f"[MISSING] {q}")

print("=== Amharic Search ===")
res = search_versions(query="Amharic")
if res:
    for b in res:
        print(f"[FOUND] Amharic -> {b['name']} ({b['id']})")
else:
    print("[MISSING] Amharic")
