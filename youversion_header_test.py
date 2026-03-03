import urllib.request
import json
import ssl

TOKEN = "PIO2wODTA5aigqMbC2WXBSpdsM1nQQExqV7mqAaNq5NqCEuF"
url = "https://api.youversion.com/v1/bibles?language_ranges[]=en"
ctx = ssl.create_default_context()

test_configs = [
    {"X-YouVersion-Developer-Token": TOKEN},
    {"Authorization": f"Bearer {TOKEN}"},
    {"Authorization": TOKEN},
    {"X-YouVersion-App-Key": TOKEN},
    {"X-API-Key": TOKEN},
    {"x-api-key": TOKEN},
    {"X-YouVersion-Client-Id": TOKEN},
    {"X-Developer-Token": TOKEN},
]

for h in test_configs:
    req = urllib.request.Request(url, headers=h)
    req.add_header("Accept", "application/json")
    hdr_name = list(h.keys())[0]
    
    try:
        with urllib.request.urlopen(req, context=ctx) as resp:
            print(f"[SUCCESS] Header: {hdr_name} | Value snippet: {h[hdr_name][:5]}...")
            print(f"Response: {resp.read().decode('utf-8')[:100]}")
            exit(0)
    except urllib.error.HTTPError as e:
        print(f"[FAIL] {hdr_name}: {e.code}")
    except Exception as e:
        print(f"[ERROR] {hdr_name}: {e}")
