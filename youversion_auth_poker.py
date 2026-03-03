import urllib.request
import json
import ssl
import sys

TOKEN = "PIO2wODTA5aigqMbC2WXBSpdsM1nQQExqV7mqAaNq5NqCEuF"
url = "https://api.youversion.com/v1/bibles?language_ranges[]=en"
ctx = ssl.create_default_context()

headers_to_try = [
    {"X-YouVersion-Developer-Token": TOKEN},
    {"Authorization": f"Bearer {TOKEN}"},
    {"X-YouVersion-App-Key": TOKEN},
    {"Ocp-Apim-Subscription-Key": TOKEN}, # Common for some APIs
    {"x-api-key": TOKEN}
]

print(f"Brute-forcing authentication headers for domain: api.youversion.com")

for h in headers_to_try:
    header_name = list(h.keys())[0]
    print(f"\nTrying header: {header_name}")
    
    req = urllib.request.Request(url, headers=h)
    req.add_header("Accept", "application/json")
    
    try:
        with urllib.request.urlopen(req, context=ctx) as response:
            print(f"  [SUCCESS] Status: {response.getcode()}")
            data = json.loads(response.read().decode('utf-8'))
            print(f"  Found {len(data.get('data', []))} bibles.")
            sys.exit(0)
    except urllib.error.HTTPError as e:
        print(f"  [FAIL] Status: {e.code}")
    except Exception as e:
        print(f"  [ERROR] {e}")

print("\nCould not authenticate with any common header.")
