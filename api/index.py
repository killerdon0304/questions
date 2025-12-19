import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from googletrans import Translator
import asyncio
import time

from indic_transliteration.sanscript import transliterate
from indic_transliteration import sanscript

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEB_DIR = os.path.join(BASE_DIR, "web")

app = FastAPI()

# ---- STATIC & TEMPLATES (FROM web/) ----
# app.mount(
 #   "/static",
  #  StaticFiles(directory=os.path.join(WEB_DIR, "static")),
  #  name="static"
#)

templates = Jinja2Templates(
    directory=os.path.join(WEB_DIR, "templates")
)

translator = Translator()


class TranslateRequest(BaseModel):
    text: str
    target_lang: str = "hi"


# -------- HINGLISH CLEANER --------
def clean_hinglish(text: str) -> str:
    return (
        text.lower()
        .replace("ā", "a")
        .replace("ī", "i")
        .replace("ū", "u")
        .replace("ṛ", "r")
        .replace("ṃ", "n")
        .replace("ṁ", "n")
        .replace("|", ".")
        .replace("’", "'")
    )


def translate_sync(text: str, dest: str, retry=3):
    if not text.strip():
        return {
            "translated": text,
            "hinglish": None,
            "detected_lang": None
        }

    actual_dest = "hi" if dest in ("hi", "bho") else dest

    for _ in range(retry):
        try:
            r = translator.translate(text, dest=actual_dest)

            hinglish = None
            if actual_dest == "hi":
                raw = transliterate(
                    r.text,
                    sanscript.DEVANAGARI,
                    sanscript.IAST
                )
                hinglish = clean_hinglish(raw)

            return {
                "translated": r.text,
                "hinglish": hinglish,
                "detected_lang": r.src
            }
        except Exception:
            time.sleep(0.5)

    return {
        "translated": text,
        "hinglish": None,
        "detected_lang": None
    }


async def translate_async(text, dest):
    return await asyncio.to_thread(translate_sync, text, dest)


@app.post("/translate")
async def translate_api(data: TranslateRequest):
    return await translate_async(data.text, data.target_lang)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request}
    )
