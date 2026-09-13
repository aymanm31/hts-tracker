import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

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

    session = requests.Session()
    retries = Retry(total=2, backoff_factor=5, status_forcelist=[429, 500, 502, 503, 504])
    session.mount("https://", HTTPAdapter(max_retries=retries))

    response = session.get(HTS_EXPORT_URL, params=params, headers=headers, timeout=(10, 60))
    response.raise_for_status()
    return response.json()