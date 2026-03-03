import urllib.request
import json
import ssl
import sys

TOKEN = "PIO2wODTA5aigqMbC2WXBSpdsM1nQQExqV7mqAaNq5NqCEuF"
ctx = ssl.create_default_context()

urls = [
    f"https://api.youversion.com/v1/bibles?language_ranges=en",
    f"https://developers.youversion.com/1.0/bibles?language_ranges[]=en",
    f"https://api.youversion.com/v1/languages"
]

headers = [
    {"X-YouVersion-Developer-Token": TOKEN},
    {"X-YouVersion-App-Key": TOKEN}
]

print("Extended YouVersion API connectivity test...")

for url in urls:
    for h in headers:
        header_name = list(h.keys())[0]
        print(f"\nURL: {url}")
        print(f"Header: {header_name}")
        
        req = urllib.request.Request(url, headers=h)
        req.add_header("Accept", "application/json")
        
        try:
            with urllib.request.urlopen(req, context=ctx) as response:
                print(f"  [SUCCESS] Status: {response.getcode()}")
                content = response.read().decode('utf-8')
                print(f"  Content length: {len(content)}")
                # If success, print first 100 chars
                print(f"  Snippet: {content[:100]}")
                sys.exit(0)
        except urllib.error.HTTPError as e:
            print(f"  [FAIL] Status: {e.code}")
        except Exception as e:
            print(f"  [ERROR] {e}")

print("\nConnectivity discovery failed.")
