import os
import json
from googletrans import Translator
from tqdm import tqdm

translator = Translator()

DATA_DIR = "data"
OUTPUT_DIR = "hindi"

SKIP_KEYS = {"correct_answer"}

ASK_MODE = True   # user se poochna hai ya nahi
GLOBAL_CHOICE = None  # y / n (all)


def translate_text(text):
    if not isinstance(text, str) or text.strip() == "":
        return text
    try:
        return translator.translate(text, src="en", dest="hi").text
    except Exception:
        return text


def translate_json(obj):
    if isinstance(obj, dict):
        result = {}
        for k, v in obj.items():
            if k in SKIP_KEYS:
                result[k] = v
            else:
                result[k] = translate_json(v)
        return result

    elif isinstance(obj, list):
        return [translate_json(item) for item in obj]

    else:
        return translate_text(obj)


def translate_large_json(data, desc):
    if isinstance(data, list):
        translated = []
        for item in tqdm(data, desc=desc, unit="item"):
            translated.append(translate_json(item))
        return translated
    return translate_json(data)


def should_translate(dest_file):
    global ASK_MODE, GLOBAL_CHOICE

    if not os.path.exists(dest_file):
        return True

    if not ASK_MODE:
        return GLOBAL_CHOICE == "y"

    print(f"\n⚠ File already translated: {os.path.basename(dest_file)}")
    choice = input("Translate again? (y = yes, n = no, a = yes to all, s = skip all): ").lower().strip()

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


def translate_file(src, dest):
    if not should_translate(dest):
        print(f"⏭ Skipped: {os.path.basename(src)}")
        return

    with open(src, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"\n🔄 Translating file: {os.path.basename(src)}")

    translated_data = translate_large_json(
        data,
        desc=os.path.basename(src)
    )

    os.makedirs(os.path.dirname(dest), exist_ok=True)

    with open(dest, "w", encoding="utf-8") as f:
        json.dump(translated_data, f, ensure_ascii=False, indent=2)

    print(f"✔ Saved: {dest}")


def main():
    if not os.path.exists(DATA_DIR):
        print("❌ data folder not found")
        return

    # Folder selection
    folders = [
        f for f in os.listdir(DATA_DIR)
        if os.path.isdir(os.path.join(DATA_DIR, f))
    ]

    print("\nAvailable folders:")
    for i, folder in enumerate(folders, 1):
        print(f"{i}. {folder}")

    folder_choice = input("\nSelect folder number: ").strip()

    try:
        folder = folders[int(folder_choice) - 1]
    except:
        print("❌ Invalid folder selection")
        return

    selected_folder_path = os.path.join(DATA_DIR, folder)

    # JSON selection
    json_files = [
        f for f in os.listdir(selected_folder_path)
        if f.endswith(".json")
    ]

    if not json_files:
        print("❌ No JSON files found")
        return

    print("\nAvailable JSON files:")
    for i, file in enumerate(json_files, 1):
        print(f"{i}. {file}")
    print("0. All JSON files")

    file_choice = input("\nSelect JSON file number: ").strip()

    if file_choice == "0":
        for file in json_files:
            src = os.path.join(selected_folder_path, file)
            dest = os.path.join(OUTPUT_DIR, folder, file)
            translate_file(src, dest)
    else:
        try:
            file = json_files[int(file_choice) - 1]
            src = os.path.join(selected_folder_path, file)
            dest = os.path.join(OUTPUT_DIR, folder, file)
            translate_file(src, dest)
        except:
            print("❌ Invalid JSON file selection")


if __name__ == "__main__":
    main()
