import requests
import random
import time


HEADERS_LIST = [
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    },
    {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0 Safari/537.36",
        "Accept-Language": "en-IN,en;q=0.9",
    }
]

session = requests.Session()
session.headers.update(random.choice(HEADERS_LIST))


def get_page(url, retries=3, delay=(1, 3)):
    """
    Polite & safe scraper with retry + backoff
    """

    for attempt in range(1, retries + 1):
        try:
            response = session.get(url, timeout=10)

            if response.status_code == 200:
                time.sleep(random.uniform(*delay))
                return response.text

            elif response.status_code == 429:
                wait = 5 * attempt
                print(f"429 Too Many Requests → waiting {wait}s")
                time.sleep(wait)

            elif response.status_code == 403:
                print("403 Forbidden → rotating headers")
                session.headers.update(random.choice(HEADERS_LIST))
                time.sleep(random.uniform(3, 6))

            else:
                print(f"HTTP {response.status_code}: {url}")
                return None

        except requests.exceptions.RequestException as e:
            wait = 2 * attempt
            print(f"Request error ({attempt}): {e}")
            time.sleep(wait)

    return None
