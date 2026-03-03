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
ctx = ssl.create_default_context()

def list_bibles(lang_code):
    url = f"https://rest.api.bible/v1/bibles?language={lang_code}"
    req = urllib.request.Request(url, headers={'api-key': API_KEY})
    try:
        with urllib.request.urlopen(req, context=ctx) as resp:
            data = json.loads(resp.read().decode('utf-8'))['data']
            return data
    except Exception as e:
        print(f"Error for {lang_code}: {e}")
        return []

print("=== Swahili (swh) versions ===")
swh_data = list_bibles("swh")
for b in swh_data:
    print(f"- {b['name']} ({b['id']})")

print("\n=== Amharic (amh) versions ===")
amh_data = list_bibles("amh")
for b in amh_data:
    print(f"- {b['name']} ({b['id']})")

print("\n=== English (eng) versions (Top 50) ===")
eng_data = list_bibles("eng")
for b in eng_data[:50]:
    print(f"- {b['name']} ({b['id']}) [Abbr: {b.get('abbreviation', 'N/A')}]")
