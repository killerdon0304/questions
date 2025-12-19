import requests

def translated(text):
    url = "https://api.mymemory.translated.net/get"
    params = {
        "q": text,
        "langpair": "en|hi"
    }

    response = requests.get(url, params=params)
    data = response.json()
    return data["responseData"]["translatedText"]



def libretranslate(text):
    url = "https://libretranslate.de/translate"
    payload = {
        "q": text,
        "source": "en",
        "target": "hi",
        "format": "text"
    }
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    data = response.json()
    return data["translatedText"]


if __name__ == "__main__":
    # Example
    print(translated("I am learning Python"))

    # Example
    print(libretranslate("How are you?"))
