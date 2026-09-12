import requests
import json

url = "https://hts.usitc.gov/reststop/exportList"
params = {
    "from": "0101",
    "to": "0105",
    "format": "JSON",
    "styles": "true"
}

response = requests.get(url, params=params, timeout=30)
response.raise_for_status()
data = response.json()

print(f"Number of records: {len(data)}")
print(json.dumps(data[0:60], indent=2))