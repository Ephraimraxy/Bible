import urllib.request
import json
import ssl

TOKEN = "PIO2wODTA5aigqMbC2WXBSpdsM1nQQExqV7mqAaNq5NqCEuF"
urls = [
    "https://developers.youversion.com/1.0/versions",
    "https://api.youversion.com/3.0/versions",
    "https://api.youversion.com/1.0/versions"
]

ctx = ssl.create_default_context()

for url in urls:
    print(f"\nTesting: {url}")
    req = urllib.request.Request(url)
    req.add_header("X-YouVersion-Developer-Token", TOKEN)
    req.add_header("Accept", "application/json")
    
    try:
        with urllib.request.urlopen(req, context=ctx) as response:
            data = json.loads(response.read().decode('utf-8'))
            print(f"Success! Found {len(data.get('versions', []))} versions.")
            break
    except Exception as e:
        print(f"Error with X-YouVersion-Developer-Token: {e}")
        
        # Try alternate header
        req2 = urllib.request.Request(url)
        req2.add_header("X-YouVersion-App-Key", TOKEN)
        req2.add_header("Accept", "application/json")
        try:
             with urllib.request.urlopen(req2, context=ctx) as response:
                data = json.loads(response.read().decode('utf-8'))
                print(f"Success with X-YouVersion-App-Key! Found {len(data.get('versions', []))} versions.")
                break
        except Exception as e2:
            print(f"Error with X-YouVersion-App-Key: {e2}")

