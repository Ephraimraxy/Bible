import urllib.request
import urllib.parse
import json
import ssl

bible_id = "0ab0c764d56a715d-02" # Hausa 66-book
API_KEY = "7uxSJHsw4Ku3hRDJHJS4X"

url = f"https://rest.api.bible/v1/bibles/{bible_id}/books"

req = urllib.request.Request(url, headers={
    'api-key': API_KEY,
    'Accept': 'application/json'
})
ctx = ssl.create_default_context()
response = urllib.request.urlopen(req, context=ctx)
books = json.loads(response.read().decode('utf-8'))['data']

print(f"Total books in Hausa: {len(books)}")
for i, b in enumerate(books):
    name = b['name'].encode('ascii', errors='replace').decode('ascii')
    print(f"{i+1}: {name} ({b['id']})")
