# import fitz  # PyMuPDF
# import json
# from pathlib import Path

# # Font sizes for heading detection
# heading_sizes = {
#     "H1": 18,
#     "H2": 14,
#     "H3": 11
# }

# def classify_heading(text_size):
#     if text_size >= heading_sizes["H1"]:
#         return "H1"
#     elif text_size >= heading_sizes["H2"]:
#         return "H2"
#     elif text_size >= heading_sizes["H3"]:
#         return "H3"
#     return None

# def process_pdf(pdf_path):
#     doc = fitz.open(pdf_path)
#     title = ""
#     outline = []

#     for page_num, page in enumerate(doc, start=1):
#         blocks = page.get_text("dict")["blocks"]
#         for block in blocks:
#             if "lines" not in block:
#                 continue
#             for line in block["lines"]:
#                 for span in line["spans"]:
#                     text = span["text"].strip()
#                     size = span["size"]

#                     if not text or len(text) < 3:
#                         continue

#                     # Set title only from page 1
#                     if page_num == 1 and size >= heading_sizes["H1"] and not title:
#                         title = text

#                     heading_level = classify_heading(size)
#                     if heading_level:
#                         print(f"Detected {heading_level}: {text} (Page {page_num})")
#                         outline.append({
#                             "level": heading_level,
#                             "text": text,
#                             "page": page_num
#                         })

#     return {
#         "title": title if title else pdf_path.stem,
#         "outline": outline
#     }

# def process_all_pdfs():
#     input_dir = Path("/app/input")
#     output_dir = Path("/app/output")
#     output_dir.mkdir(parents=True, exist_ok=True)

#     for pdf_file in input_dir.glob("*.pdf"):
#         print(f"Processing: {pdf_file.name}")
#         result = process_pdf(pdf_file)
#         output_file = output_dir / f"{pdf_file.stem}.json"
#         with open(output_file, "w", encoding="utf-8") as f:
#             json.dump(result, f, indent=2)

# if __name__ == "__main__":
#     process_all_pdfs()

import fitz  # PyMuPDF
import json
import time
from pathlib import Path

# Constants for heading classification
HEADING_SIZES = {
    "H1": 18,
    "H2": 14,
    "H3": 11
}

# Fallback: if size classification fails, use bold/caps
FALLBACK_FLAG_BOLD = 20


def classify_heading(size, flags, text):
    if size >= HEADING_SIZES["H1"]:
        return "H1"
    elif size >= HEADING_SIZES["H2"]:
        return "H2"
    elif size >= HEADING_SIZES["H3"]:
        return "H3"
    elif flags == FALLBACK_FLAG_BOLD or text.isupper():
        return "H3"  # Fallback as minor heading
    return None


def extract_title_from_first_page(page):
    blocks = page.get_text("dict")["blocks"]
    for block in blocks:
        if "lines" not in block:
            continue
        for line in block["lines"]:
            for span in line["spans"]:
                text = span["text"].strip()
                if text and span["size"] >= HEADING_SIZES["H1"]:
                    return text
    return "Untitled Document"


def extract_headings(doc):
    headings = []
    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                for span in line["spans"]:
                    text = span["text"].strip()
                    if not text or len(text) < 3:
                        continue
                    heading_level = classify_heading(span["size"], span["flags"], text)
                    if heading_level:
                        headings.append({
                            "level": heading_level,
                            "text": text,
                            "page": page_num
                        })
    return headings


def process_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"[ERROR] Failed to open {pdf_path.name}: {e}")
        return {"title": pdf_path.stem, "outline": []}

    title = extract_title_from_first_page(doc[0])
    headings = extract_headings(doc)

    return {
        "title": title,
        "outline": headings
    }


def save_output_to_json(data, output_path):
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"[INFO] Output saved to {output_path.name}")
    except Exception as e:
        print(f"[ERROR] Failed to write JSON: {e}")


# ---------------- Main CLI Execution ----------------
if __name__ == "__main__":
    INPUT_DIR = Path("input")
    OUTPUT_DIR = Path("output")
    OUTPUT_DIR.mkdir(exist_ok=True)

    for pdf_file in INPUT_DIR.glob("*.pdf"):
        print(f"\n[PROCESSING] {pdf_file.name}")
        start = time.time()

        result = process_pdf(pdf_file)

        output_file = OUTPUT_DIR / f"{pdf_file.stem}.json"
        save_output_to_json(result, output_file)

        print(f"[DONE] {pdf_file.name} in {time.time() - start:.2f} sec")
