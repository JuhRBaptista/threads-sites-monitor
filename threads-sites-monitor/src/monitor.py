import time
import requests

def check_site(url):
    try:
        start = time.time()
        response = requests.get(url, timeout=5)
        end = time.time()
        status = "OK" if response.status_code == 200 else f"ERRO ({response.status_code})"
        duration = round((end - start) * 1000)
    except Exception:
        status = "ERRO"
        duration = "-"
    return url, status, duration