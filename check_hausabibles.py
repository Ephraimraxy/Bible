import urllib.request
import json
import ssl
import sys

# Force UTF-8 output
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except AttributeError:
    pass

API_KEY = "7uxSJHsw4Ku3hRDJHJS4X"
url = "https://rest.api.bible/v1/bibles?language=hau"

req = urllib.request.Request(url, headers={'api-key': API_KEY})
ctx = ssl.create_default_context()

try:
    with urllib.request.urlopen(req, context=ctx) as response:
        data = json.loads(response.read().decode('utf-8'))['data']
        print(f"Found {len(data)} Hausa Bibles:")
        for bible in data:
            bid = bible['id']
            name = bible['name']
            
            # Fetch book count for this bible
            book_url = f"https://rest.api.bible/v1/bibles/{bid}/books"
            book_req = urllib.request.Request(book_url, headers={'api-key': API_KEY})
            try:
                with urllib.request.urlopen(book_req, context=ctx) as book_resp:
                    books = json.loads(book_resp.read().decode('utf-8'))['data']
                    print(f"- {name} ({bid}): {len(books)} books")
            except Exception as e:
                print(f"- {name} ({bid}): Error fetching books: {e}")
except Exception as e:
    print(f"Error fetching bibles: {e}")
