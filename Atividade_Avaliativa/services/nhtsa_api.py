import requests

BASE = "https://vpic.nhtsa.dot.gov/api/vehicles"


def modelos_por_marca(marca: str):
    url = f"{BASE}/GetModelsForMake/{marca}"
    r = requests.get(url, params={"format": "json"}, timeout=10)
    r.raise_for_status()
    return [item["Model_Name"] for item in r.json().get("Results", [])]
    
