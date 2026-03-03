import urllib.request
import json
import ssl
import sys

# Force UTF-8 output
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except AttributeError:
    pass

TOKEN = "PIO2wODTA5aigqMbC2WXBSpdsM1nQQExqV7mqAaNq5NqCEuF"
BASE_URL = "https://api.youversion.com"

def test_youversion():
    ctx = ssl.create_default_context()
    
    # Try fetching English bibles first
    languages = ["en", "sw", "am", "*"]
    
    for lang in languages:
        url = f"{BASE_URL}/v1/bibles?language_ranges[]={lang}"
        print(f"\nTesting Language Range: {lang}")
        print(f"URL: {url}")
        
        req = urllib.request.Request(url)
        req.add_header("X-YouVersion-Developer-Token", TOKEN)
        req.add_header("Accept", "application/json")
        
        try:
            with urllib.request.urlopen(req, context=ctx) as response:
                status = response.getcode()
                content = response.read().decode('utf-8')
                if status == 200:
                    data = json.loads(content)
                    bibles = data.get('data', [])
                    print(f"Success! Found {len(bibles)} Bibles.")
                    for b in bibles[:20]:
                        print(f"- [{b.get('id')}] {b.get('title')} ({b.get('abbreviation')})")
                else:
                    print(f"Status: {status}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_youversion()
