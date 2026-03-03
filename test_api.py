"""
Testing API.bible connectivity with various endpoint formats.
"""
import urllib.request
import json
import ssl

API_KEY = "RMTurJIneoNdm1SCzKofW"

# Try different endpoint formats
endpoints = [
    "https://rest.api.bible/v1/bibles",
    "https://api.scripture.api.bible/v1/bibles",
]

for url in endpoints:
    print(f"\nTrying: {url}")
    try:
        req = urllib.request.Request(url, headers={
            'api-key': API_KEY,
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0'
        })
        # Create an SSL context that doesn't verify (in case of cert issues)
        ctx = ssl.create_default_context()
        response = urllib.request.urlopen(req, context=ctx)
        data = json.loads(response.read().decode('utf-8'))
        bibles = data.get("data", [])
        print(f"  SUCCESS! {len(bibles)} Bibles available")
        # Print first 3 as sample
        for b in bibles[:3]:
            print(f"  - {b.get('id')}: {b.get('name')} ({b.get('language',{}).get('name','')})")
        break
    except Exception as e:
        print(f"  FAILED: {e}")
