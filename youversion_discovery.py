import urllib.request
import json
import ssl

TOKEN = "PIO2wODTA5aigqMbC2WXBSpdsM1nQQExqV7mqAaNq5NqCEuF"

# Potential endpoints based on various documentation snippets
bases = [
    "https://api.youversion.com/v3",
    "https://api.youversion.com/v2",
    "https://api.youversion.com/v1",
    "https://developers.youversion.com/api/v3",
    "https://developers.youversion.com/1.0"
]

paths = [
    "/bible/versions",
    "/bibles",
    "/versions",
    "/bible/languages"
]

header_keys = [
    "X-YouVersion-Developer-Token",
    "Authorization",
    "X-YouVersion-App-Key",
    "X-API-Key"
]

ctx = ssl.create_default_context()

for base in bases:
    for path in paths:
        url = base + path
        print(f"Testing URL: {url}")
        
        for h_key in header_keys:
            h_val = TOKEN
            if h_key == "Authorization":
                h_val = f"Bearer {TOKEN}"
            
            req = urllib.request.Request(url)
            req.add_header(h_key, h_val)
            req.add_header("Accept", "application/json")
            
            try:
                with urllib.request.urlopen(req, context=ctx) as resp:
                    data = json.loads(resp.read().decode('utf-8'))
                    print(f"  [SUCCESS] Header: {h_key} | Results: {len(data)}")
                    # If success, stop
                    exit(0)
            except urllib.error.HTTPError as e:
                # print(f"  [FAIL] {h_key}: {e.code}")
                pass
            except Exception as e:
                # print(f"  [FAIL] {h_key}: {e}")
                pass

print("\nAll guessed combinations failed.")
