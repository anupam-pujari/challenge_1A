import os
import json
from utils import extract_headings
INPUT_DIR = "./input"
OUTPUT_DIR = "./output"
def process_all_pdfs():
    for filename in os.listdir(INPUT_DIR):
        if filename.endswith(".pdf"):
            input_path = os.path.join(INPUT_DIR, filename)
            title, outline = extract_headings(input_path)
            output = {"title": title or "Untitled Document", "outline": outline}

            output_filename = filename.replace(".pdf", ".json")
            output_path = os.path.join(OUTPUT_DIR, output_filename)
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(output, f, indent=2, ensure_ascii=False)
if __name__ == "__main__":
    process_all_pdfs()
