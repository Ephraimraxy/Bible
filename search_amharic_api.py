import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
# The language code for Amharic is usually 'amh' or 'am'
url = 'https://api.scripture.api.bible/v1/bibles?language=amh'
# Also try 'am'
# url = 'https://api.scripture.api.bible/v1/bibles?language=am'

api_key = 'uesz2-G0D2gZ0Pnwk2Hgp'

def search_bibles(lang):
    search_url = f'https://api.scripture.api.bible/v1/bibles?language={lang}'
    print(f"Searching for {lang}...")
    req = urllib.request.Request(search_url, headers={'api-key': api_key})
    try:
        with urllib.request.urlopen(req, context=ctx) as resp:
            data = json.loads(resp.read())
            bibles = data.get('data', [])
            for b in bibles:
                print(f"ID: {b['id']}, Name: {b['name']}, Abbreviation: {b['abbreviation']}")
    except Exception as e:
        print(f"Error for {lang}: {e}")

if __name__ == "__main__":
    search_bibles('amh')
    search_bibles('am')
