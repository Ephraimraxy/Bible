import urllib.request
import urllib.parse
import json
import ssl

bible_id = "0ab0c764d56a715d-01" # Hausa
API_KEY = "7uxSJHsw4Ku3hRDJHJS4X"
book_api_id = "REV" 

# First find the actual book ID. Hausa might use non-standard book IDs
url = f"https://rest.api.bible/v1/bibles/{bible_id}/books"

req = urllib.request.Request(url, headers={
    'api-key': API_KEY,
    'Accept': 'application/json'
})
ctx = ssl.create_default_context()
response = urllib.request.urlopen(req, context=ctx)
books = json.loads(response.read().decode('utf-8'))['data']

target_id = None
for b in books:
    if "Ru" in b['name'] or b['name'] == "Ruʼuya ta Yohanna":
        target_id = b['id']
        print(f"Hausa book: {b['name'].encode('ascii', errors='replace').decode('ascii')} -> ID: {b['id']}")

if target_id:
    # Fetch chapters
    path = f"/bibles/{bible_id}/books/{target_id}/chapters"
    safe_path = urllib.parse.quote(path, safe='/?=&')
    url = "https://rest.api.bible/v1" + safe_path
    
    req = urllib.request.Request(url, headers={
        'api-key': API_KEY,
        'Accept': 'application/json'
    })
    response = urllib.request.urlopen(req, context=ctx)
    chaps = json.loads(response.read().decode('utf-8'))['data']
    print(f"Found {len(chaps)} chapters")
    for c in chaps[:3]:
        chap_id = c['id']
        chap_num_raw = c.get('number')
        print(f"Fetching chapter content for {chap_id}... chap_num_raw='{chap_num_raw}'")
        
        try:
            int(chap_num_raw)
        except Exception as e:
            print(f"  -> int() cast failed: {e}")
else:
    print("Book not found")
