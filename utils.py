import fitz
from collections import defaultdict


def extract_headings(pdf_path):
    doc = fitz.open(pdf_path)
    font_sizes = defaultdict(list)

    outline = []
    title = None

    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                line_text = ""
                max_size = 0
                for span in line["spans"]:
                    text = span["text"].strip()
                    if not text:
                        continue
                    size = round(span["size"], 1)
                    max_size = max(max_size, size)
                    line_text += text + " " 

                line_text = line_text.strip()
                if len(line_text) >= 5:  
                    font_sizes[max_size].append((line_text, page_num))

    sorted_sizes = sorted(font_sizes.keys(), reverse=True)

    if sorted_sizes:
        title_candidates = font_sizes[sorted_sizes[0]]
        if title_candidates:
            title_lines = [text for text, _ in title_candidates if len(text) > 3]
            title = " ".join(title_lines).strip()

        for idx, size in enumerate(sorted_sizes[1:4]): 
            level = f"H{idx+1}"
            for text, page in font_sizes[size]:
                outline.append({"level": level, "text": text, "page": page})

    return title, outline
