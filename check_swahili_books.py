import urllib.request
import json
import ssl

API_KEY = "7uxSJHsw4Ku3hRDJHJS4X"
bible_id = "611f8eb23aec8f13-01" # Swahili

url = f"https://rest.api.bible/v1/bibles/{bible_id}/books"
req = urllib.request.Request(url, headers={'api-key': API_KEY})
ctx = ssl.create_default_context()

try:
    with urllib.request.urlopen(req, context=ctx) as resp:
        data = json.loads(resp.read().decode('utf-8'))['data']
        print(f"Swahili (SWA) has {len(data)} books.")
        for b in data[:5]:
            print(f"- {b['name']} ({b['id']})")
        if len(data) >= 66:
            print("[SUCCESS] Full Bible detected.")
        else:
            print("[NOTICE] Potentially incomplete or NT only.")
except Exception as e:
    print(f"Error: {e}")
