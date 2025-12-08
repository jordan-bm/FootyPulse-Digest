import requests

API_KEY = "4b2b659702151bd1f9e338bdbacee43f"   # <-- replace with your actual key

url = "https://v3.football.api-sports.io/status"
headers = {
    "x-apisports-key": API_KEY
}



resp = requests.get(url, headers=headers).json()
print(resp)
