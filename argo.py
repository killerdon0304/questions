import os
import json
from tqdm import tqdm
from multiprocessing import Pool, cpu_count
from argostranslate import translate

DATA_DIR = "data"
OUTPUT_DIR = "argohindi"
CACHE_FILE = "sentence_cache.json"

SKIP_KEYS = {"correct_answer"}

ASK_MODE = True
GLOBAL_CHOICE = None

# ---------------- CACHE ---------------- #

if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        SENTENCE_CACHE = json.load(f)
else:
    SENTENCE_CACHE = {}

def save_cache():
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(SENTENCE_CACHE, f, ensure_ascii=False, indent=2)

# ---------------- TRANSLATION ---------------- #

def translate_text(text):
    if not isinstance(text, str) or not text.strip():
        return text

    if text in SENTENCE_CACHE:
        return SENTENCE_CACHE[text]

    translated = translate.translate(text, "en", "hi")
    SENTENCE_CACHE[text] = translated
    return translated

def translate_json(obj):
    if isinstance(obj, dict):
        return {
            k: v if k in SKIP_KEYS else translate_json(v)
            for k, v in obj.items()
        }
    elif isinstance(obj, list):
        return [translate_json(i) for i in obj]
    else:
        return translate_text(obj)

def process_item(item):
    return translate_json(item)

# ---------------- SKIP LOGIC ---------------- #

def should_translate(dest_file):
    global ASK_MODE, GLOBAL_CHOICE

    if not os.path.exists(dest_file):
        return True

    if not ASK_MODE:
        return GLOBAL_CHOICE == "y"

    print(f"\n⚠ File already translated: {os.path.basename(dest_file)}")
    choice = input(
        "Translate again? (y = yes, n = no, a = yes to all, s = skip all): "
    ).lower().strip()

    if choice == "a":
        ASK_MODE = False
        GLOBAL_CHOICE = "y"
        return True
    elif choice == "s":
        ASK_MODE = False
        GLOBAL_CHOICE = "n"
        return False
    elif choice == "y":
        return True
    else:
        return False

# ---------------- RESUME ---------------- #

def get_resume_index(resume_file):
    if os.path.exists(resume_file):
        try:
            with open(resume_file, "r") as f:
                return int(f.read().strip())
        except:
            return 0
    return 0

def save_resume_index(resume_file, index):
    with open(resume_file, "w") as f:
        f.write(str(index))

# ---------------- FILE TRANSLATION ---------------- #

def translate_file(src, dest):
    if not should_translate(dest):
        print(f"⏭ Skipped: {os.path.basename(src)}")
        return

    with open(src, "r", encoding="utf-8") as f:
        data = json.load(f)

    os.makedirs(os.path.dirname(dest), exist_ok=True)
    resume_file = dest + ".resume"

    if isinstance(data, list):
        start = get_resume_index(resume_file)
        remaining = data[start:]
        workers = max(1, cpu_count() - 1)

        translated = []
        with Pool(workers) as pool:
            for idx, result in enumerate(
                tqdm(
                    pool.imap(process_item, remaining),
                    total=len(remaining),
                    desc=os.path.basename(src),
                    unit="item"
                ),
                start=start
            ):
                translated.append(result)
                save_resume_index(resume_file, idx + 1)

        final_data = data[:start] + translated

        if os.path.exists(resume_file):
            os.remove(resume_file)
    else:
        final_data = translate_json(data)

    with open(dest, "w", encoding="utf-8") as f:
        json.dump(final_data, f, ensure_ascii=False, indent=2)

    save_cache()
    print(f"✔ Saved: {dest}")

# ---------------- MAIN (FIXED FLOW) ---------------- #

def main():
    # Folder select
    folders = [
        f for f in os.listdir(DATA_DIR)
        if os.path.isdir(os.path.join(DATA_DIR, f))
    ]

    print("\nAvailable folders:")
    for i, f in enumerate(folders, 1):
        print(f"{i}. {f}")

    folder = folders[int(input("\nSelect folder number: ")) - 1]
    folder_path = os.path.join(DATA_DIR, folder)

    # File select (with ALL option)
    json_files = [f for f in os.listdir(folder_path) if f.endswith(".json")]

    print("\nAvailable JSON files:")
    for i, f in enumerate(json_files, 1):
        print(f"{i}. {f}")
    print("0. All JSON files")

    choice = input("\nSelect JSON file: ").strip()

    if choice == "0":
        for f in json_files:
            translate_file(
                os.path.join(folder_path, f),
                os.path.join(OUTPUT_DIR, folder, f)
            )
    else:
        f = json_files[int(choice) - 1]
        translate_file(
            os.path.join(folder_path, f),
            os.path.join(OUTPUT_DIR, folder, f)
        )

if __name__ == "__main__":
    main()
