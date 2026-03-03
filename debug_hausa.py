import urllib.request
import json
import ssl

bible_id = "0ab0c764d56a715d-01" # Hausa
API_KEY = "7uxSJHsw4Ku3hRDJHJS4X"
url = f"https://rest.api.bible/v1/bibles/{bible_id}/books"

req = urllib.request.Request(url, headers={
    'api-key': API_KEY,
    'Accept': 'application/json'
})
ctx = ssl.create_default_context()
response = urllib.request.urlopen(req, context=ctx)
books = json.loads(response.read().decode('utf-8'))['data']

for b in books:
    if "Ru" in b['name'] or b['name'] == "Ruʼuya ta Yohanna":
        print(f"Hausa book: {b['name']} -> ID: {b['id']}")

# Fetch chapters for REV
url = f"https://rest.api.bible/v1/bibles/{bible_id}/books/REV/chapters"
req = urllib.request.Request(url, headers={
    'api-key': API_KEY,
    'Accept': 'application/json'
})
response = urllib.request.urlopen(req, context=ctx)
print(response.read().decode('utf-8'))
