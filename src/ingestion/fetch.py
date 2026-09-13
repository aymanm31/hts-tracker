import requests

HTS_EXPORT_URL = "https://hts.usitc.gov/reststop/exportList"


def fetch_hts(from_code="0101", to_code="9999"):
    params = {
        "from": from_code,
        "to": to_code,
        "format": "JSON",
        "styles": "true",
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; hts-tracker/1.0)"
    }
    response = requests.get(HTS_EXPORT_URL, params=params, headers=headers, timeout=(10, 30))
    response.raise_for_status()
    return response.json()