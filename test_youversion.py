import urllib.request
import json
import ssl

TOKEN = "PIO2wODTA5aigqMbC2WXBSpdsM1nQQExqV7mqAaNq5NqCEuF"
url = "https://developers.youversionapi.com/1.0/versions"

req = urllib.request.Request(url)
req.add_header("X-YouVersion-Developer-Token", TOKEN)
req.add_header("Accept", "application/json")

ctx = ssl.create_default_context()

print(f"Testing YouVersion API Key...")
try:
    with urllib.request.urlopen(req, context=ctx) as response:
        data = json.loads(response.read().decode('utf-8'))
        print("Success! Connection established.")
        print(f"Found {len(data.get('versions', []))} versions.")
        for v in data.get('versions', [])[:10]:
            print(f"- {v.get('title')} ({v.get('id')})")
except Exception as e:
    print(f"Error: {e}")
    # Try alternate header if first one fails
    print("\nTrying alternate header (X-YouVersion-App-Key)...")
    req2 = urllib.request.Request(url)
    req2.add_header("Accept", "application/json")
    req2.add_header("X-YouVersion-App-Key", TOKEN)
    try:
         with urllib.request.urlopen(req2, context=ctx) as response:
            data = json.loads(response.read().decode('utf-8'))
            print("Success with App-Key!")
    except Exception as e2:
        print(f"Error with App-Key: {e2}")

