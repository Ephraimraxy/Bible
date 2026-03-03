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

def search_paginated():
    ctx = ssl.create_default_context()
    
    requested_terms = ["New International", "King James", "Living", "Standard", "Message", "Good News", "Swahili", "Amharic", "Amplified"]
    found_versions = []
    
    page_token = ""
    page_count = 0
    
    while True:
        page_count += 1
        url = f"{BASE_URL}/v1/bibles?language_ranges[]=*&all_available=true&page_size=100"
        if page_token:
            url += f"&page_token={page_token}"
            
        print(f"Fetching page {page_count}...")
        
        req = urllib.request.Request(url)
        req.add_header(HEADER_NAME, TOKEN)
        req.add_header("Accept", "application/json")
        
        try:
            with urllib.request.urlopen(req, context=ctx) as response:
                data = json.loads(response.read().decode('utf-8'))
                bibles = data.get('data', [])
                
                for b in bibles:
                    title = b.get('title', '')
                    abbr = b.get('abbreviation', '')
                    vid = b.get('id')
                    lang = b.get('language_tag', '')
                    
                    for term in requested_terms:
                        if term.lower() in title.lower() or term.lower() in abbr.lower():
                            found_versions.append(f"[{vid}] {title} ({abbr}) [{lang}]")
                
                page_token = data.get('next_page_token')
                if not page_token or page_count > 20: # Safety break anyway
                    break
        except Exception as e:
            print(f"Error on page {page_count}: {e}")
            break

    print("\n=== Search Results (Total Found: {}) ===".format(len(found_versions)))
    unique_results = sorted(list(set(found_versions)))
    for res in unique_results:
        print(f"  {res}")

if __name__ == "__main__":
    search_paginated()
