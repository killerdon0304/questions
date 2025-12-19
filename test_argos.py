import os
import json
import time
from googletrans import Translator
from tqdm import tqdm

translator = Translator()

DATA_DIR = "data"
OUTPUT_DIR = "hindi"

SKIP_KEYS = {"correct_answer"}

ASK_MODE = True
GLOBAL_CHOICE = None


# ---------------- TRANSLATION ---------------- #

def translate_text(text, retry=3):
    if not isinstance(text, str) or not text.strip():
        return text

    for _ in range(retry):
        try:
            return translator.translate(text, src="en", dest="hi").text
        except Exception:
            time.sleep(1)

    return text


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


# ---------------- RESUME SUPPORT ---------------- #

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
    start_index = 0

    # Resume only for list JSON
    if isinstance(data, list):
        start_index = get_resume_index(resume_file)

        if start_index > 0:
            print(f"▶ Resuming from item {start_index}")

        output = []

        # load already translated part if exists
        if os.path.exists(dest):
            try:
                with open(dest, "r", encoding="utf-8") as f:
                    output = json.load(f)
            except:
                output = []

        for idx in tqdm(range(start_index, len(data)),
                        desc=os.path.basename(src),
                        unit="item"):
            translated_item = translate_json(data[idx])
            output.append(translated_item)
            save_resume_index(resume_file, idx + 1)

        translated_data = output

        if os.path.exists(resume_file):
            os.remove(resume_file)

    else:
        translated_data = translate_json(data)

    with open(dest, "w", encoding="utf-8") as f:
        json.dump(translated_data, f, ensure_ascii=False, indent=2)

    print(f"✔ Saved: {dest}")


# ---------------- MAIN ---------------- #

def main():
    folders = [
        f for f in os.listdir(DATA_DIR)
        if os.path.isdir(os.path.join(DATA_DIR, f))
    ]

    print("\nAvailable folders:")
    for i, f in enumerate(folders, 1):
        print(f"{i}. {f}")

    folder = folders[int(input("\nSelect folder number: ")) - 1]
    folder_path = os.path.join(DATA_DIR, folder)

    json_files = [f for f in os.listdir(folder_path) if f.endswith(".json")]

    print("\nAvailable JSON files:")
    for i, f in enumerate(json_files, 1):
        print(f"{i}. {f}")
    print("0. All JSON files")

    choice = input("\nSelect JSON file: ")

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
