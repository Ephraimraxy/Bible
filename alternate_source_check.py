import urllib.request
import ssl

ctx = ssl.create_default_context()

# Various potential open-source Bible URLs (JSON/USFM/Plain)
check_urls = [
    "https://raw.githubusercontent.com/gratis-bible/bible/master/json/am-amh.json",
    "https://raw.githubusercontent.com/gratis-bible/bible/master/json/am-nasv.json",
    "https://raw.githubusercontent.com/BibleZ/biblez-translations/master/bibles/am_amh.json",
    "https://raw.githubusercontent.com/BibleZ/biblez-translations/master/bibles/amh.json",
    "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/en_nkjv.json",
    "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/en_niv.json",
    "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/en_esv.json",
    "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/en_nlt.json",
    "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/en_gnt.json",
    "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/en_cev.json",
    "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/en_nasb.json",
    "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/en_amp.json",
    "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/en_msg.json",
]

print("Checking alternative source URLs for Amharic and English versions...")
for url in check_urls:
    try:
        req = urllib.request.Request(url, method='HEAD')
        with urllib.request.urlopen(req, context=ctx) as resp:
            print(f"[FOUND] {url}")
    except Exception:
        # print(f"[MISSING] {url}")
        pass
