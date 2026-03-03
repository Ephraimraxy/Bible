import urllib.request
import json
import ssl

TOKEN = "PIO2wODTA5aigqMbC2WXBSpdsM1nQQExqV7mqAaNq5NqCEuF"
url = "https://api.youversion.com/v1/bibles?language_ranges%5B%5D=*"
ctx = ssl.create_default_context()

headers = {
    "X-YouVersion-Developer-Token": TOKEN,
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

print(f"Testing URL: {url}")
req = urllib.request.Request(url, headers=headers)

try:
    with urllib.request.urlopen(req, context=ctx) as resp:
        print(f"[SUCCESS] Status: {resp.getcode()}")
        print(f"Data: {resp.read().decode('utf-8')[:500]}")
except urllib.error.HTTPError as e:
    print(f"[FAIL] Status: {e.code}")
    print(f"Body: {e.read().decode('utf-8')}")
except Exception as e:
    print(f"[ERROR] {e}")
