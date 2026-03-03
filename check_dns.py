import socket

domains = [
    "developers.youversionapi.com",
    "api.youversionapi.com",
    "yv-api.youversionapi.com",
    "youversionapi.com",
    "api.youversion.com",
    "developers.youversion.com"
]

for d in domains:
    try:
        ip = socket.gethostbyname(d)
        print(f"[SUCCESS] {d} -> {ip}")
    except socket.gaierror:
        print(f"[FAILED] {d}")
