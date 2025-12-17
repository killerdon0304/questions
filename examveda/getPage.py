
import requests
import random
import time


# def get_page(url):
#     response = requests.get(url)
#     if response.status_code == 200:
#         return response.text
#     else:
#         return None



HEADERS_LIST = [
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/",
    },
    {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0 Safari/537.36",
        "Accept-Language": "en-IN,en;q=0.9",
        "Referer": "https://www.bing.com/",
    }
]

session = requests.Session()

def get_page(url, retries=3, delay=(1, 3)):
    """
    Polite & safe scraper
    """

    for attempt in range(retries):
        try:
            headers = random.choice(HEADERS_LIST)

            response = session.get(
                url,
                headers=headers,
                timeout=10
            )

            # ✔ success
            if response.status_code == 200:
                time.sleep(random.uniform(*delay))  # rate limit
                return response.text

            # ❌ blocked / forbidden
            elif response.status_code in [403, 429]:
                print(f"Blocked ({response.status_code}), retrying...")
                time.sleep(random.uniform(5, 8))

            else:
                print(f"HTTP {response.status_code} for {url}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            time.sleep(random.uniform(2, 5))

    return None
