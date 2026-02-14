import requests
BASE = "http://localhost:8000/api"
r = requests.get(BASE + "/notifications/")
print(f"Status: {r.status_code}")
print(f"Response: {r.text[:200]}")