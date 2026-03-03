import urllib.request
import json
import ssl

TOKEN = "PIO2wODTA5aigqMbC2WXBSpdsM1nQQExqV7mqAaNq5NqCEuF"
BASE_URL = "https://api.youversion.com"
HEADER_NAME = "X-YVP-App-Key"

# Test IDs found:
# 111: NIV 2011
# 1588: AMP
# 1627: Swahili (NEN)
# 1260: Amharic (NASV)
# 1: KJV

test_cases = [
    (1, "GEN.1.1", "KJV"),
    (111, "GEN.1.1", "NIV"),
    (1588, "GEN.1.1", "AMP"),
    (1627, "GEN.1.1", "SWA"),
    (1260, "GEN.1.1", "AMH")
]

ctx = ssl.create_default_context()

for vid, passage, label in test_cases:
    url = f"{BASE_URL}/v1/bibles/{vid}/passages/{passage}?format=text"
    print(f"\nTesting {label} (ID: {vid}) - Passage: {passage}")
    
    req = urllib.request.Request(url)
    req.add_header(HEADER_NAME, TOKEN)
    req.add_header("Accept", "application/json")
    
    try:
        with urllib.request.urlopen(req, context=ctx) as response:
            data = json.loads(response.read().decode('utf-8'))
            content = data.get('content', '')
            print(f"  [SUCCESS] Content: {content[:100]}...")
    except Exception as e:
        print(f"  [FAIL] {e}")
