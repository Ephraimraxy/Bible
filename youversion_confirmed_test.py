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

# The error message revealed the correct header!
# "Failed to resolve API Key variable request.header.x-yvp-app-key"
HEADER_NAME = "X-YVP-App-Key"

def list_youversion_bibles(lang_range):
    url = f"{BASE_URL}/v1/bibles?language_ranges[]={lang_range}"
    print(f"\nListing Bibles for: {lang_range}")
    
    req = urllib.request.Request(url)
    req.add_header(HEADER_NAME, TOKEN)
    req.add_header("Accept", "application/json")
    
    ctx = ssl.create_default_context()
    
    try:
        with urllib.request.urlopen(req, context=ctx) as response:
            data = json.loads(response.read().decode('utf-8'))
            bibles = data.get('data', [])
            print(f"  [OK] Found {len(bibles)} versions.")
            for b in bibles:
                # Print ID, Abbr, and Title
                print(f"  - [{b.get('id')}] {b.get('title')} ({b.get('abbreviation')})")
            return bibles
    except Exception as e:
        print(f"  [FAIL] {e}")
        return []

if __name__ == "__main__":
    # Test with English
    list_youversion_bibles("en")
    # Test with Swahili
    list_youversion_bibles("sw")
    # Test with Amharic
    list_youversion_bibles("am")
