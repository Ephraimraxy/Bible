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
HEADER_NAME = "X-YVP-App-Key"

def search_full_catalog():
    ctx = ssl.create_default_context()
    
    # Request all available versions across all languages
    url = f"{BASE_URL}/v1/bibles?language_ranges[]=*&all_available=true"
    print(f"Searching Full YouVersion Catalog: {url}")
    
    req = urllib.request.Request(url)
    req.add_header(HEADER_NAME, TOKEN)
    req.add_header("Accept", "application/json")
    
    requested = ["NIV", "NKJV", "ESV", "NLT", "MSG", "GNT", "CEV", "NASB", "AMP", "SWA", "AMH"]
    found = {}

    try:
        with urllib.request.urlopen(req, context=ctx) as response:
            data = json.loads(response.read().decode('utf-8'))
            bibles = data.get('data', [])
            print(f"Total Bibles found in platform: {data.get('total_size', len(bibles))}")
            
            for b in bibles:
                title = b.get('title', '')
                abbr = b.get('abbreviation', '')
                vid = b.get('id')
                lang = b.get('language_tag', '')
                
                # Check for requested versions
                for r in requested:
                    if r.lower() == abbr.lower() or r.lower() in title.lower():
                        if r not in found: found[r] = []
                        found[r].append(f"[{vid}] {title} ({abbr}) [{lang}]")
            
            print("\n=== Search Results for Requested Versions ===")
            for r in requested:
                if r in found:
                    print(f"\n{r}:")
                    for match in found[r]:
                        print(f"  - {match}")
                else:
                    print(f"\n{r}: NOT FOUND")
                    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    search_full_catalog()
