import os
import json
import re

def save_questions_to_json(questions, category, name=None):
    """
    questions : list
    category  : folder name (e.g. History)
    name      : json file name (optional)
    """

    # 🔹 Base directory = parent of current file
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    DATA_DIR = os.path.join(BASE_DIR, "data")

    # 🔹 Case 1: name diya gaya → data/History/name.json
    if name:
        safe_name = re.sub(r'[\\/*?:"<>|]', '', name)

        folder_path = os.path.join(DATA_DIR, category)
        os.makedirs(folder_path, exist_ok=True)

        file_path = os.path.join(folder_path, f"{safe_name}.json")

    # 🔹 Case 2: name nahi diya → data/history.json
    else:
        safe_category = re.sub(r'[\\/*?:"<>|]', '', category.lower())
        os.makedirs(DATA_DIR, exist_ok=True)

        file_path = os.path.join(DATA_DIR, f"{safe_category}.json")

    # 🔹 Write JSON
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(questions, f, ensure_ascii=False, indent=4)

    return file_path
