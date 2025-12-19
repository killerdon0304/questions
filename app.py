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

app = FastAPI(title="Translator App")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

translator = Translator()


class TranslateRequest(BaseModel):
    text: str
    target_lang: str = "hi"


# -------- HINGLISH CLEANER (IMPORTANT) -------- #
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
            "detected_lang": None,
            "translated": text,
            "hinglish": None
        }

    # Bhojpuri → Hindi fallback
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
                "detected_lang": r.src,
                "translated": r.text,
                "hinglish": hinglish
            }
        except Exception:
            time.sleep(0.5)

    return {
        "detected_lang": None,
        "translated": text,
        "hinglish": None
    }


async def translate_async(text: str, dest: str):
    return await asyncio.to_thread(translate_sync, text, dest)


@app.post("/translate")
async def translate_api(data: TranslateRequest):
    return await translate_async(data.text, data.target_lang)


@app.get("/", response_class=HTMLResponse)
async def ui(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
