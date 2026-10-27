import json
import re
from pathlib import Path

from pypdf import PdfReader


PROJECT_ROOT = Path(__file__).resolve().parents[2]
REGULATIONS_DIR = PROJECT_ROOT / "corpus" / "regulations"
OUTPUT_FILE = PROJECT_ROOT / "corpus" / "processed" / "regulation_chunks.json"

CHUNK_SIZE = 1200
CHUNK_OVERLAP = 200


def clean_text(text: str) -> str:
    """Normalize whitespace without removing clause references."""
    text = text.replace("\x00", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def split_into_chunks(text: str):
    """Split extracted text into overlapping character-based chunks."""
    chunks = []
    start = 0

    while start < len(text):
        end = min(start + CHUNK_SIZE, len(text))

        # Prefer ending at a word boundary.
        if end < len(text):
            boundary = text.rfind(" ", start, end)
            if boundary > start:
                end = boundary

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start = max(end - CHUNK_OVERLAP, start + 1)

    return chunks


def main():
    if not REGULATIONS_DIR.exists():
        raise FileNotFoundError(
            f"Regulations folder not found: {REGULATIONS_DIR}"
        )

    pdf_files = sorted(REGULATIONS_DIR.glob("*.pdf"))

    if not pdf_files:
        raise FileNotFoundError(
            f"No PDF files found in {REGULATIONS_DIR}. "
            "Place your official regulations PDF in that folder."
        )

    records = []

    for pdf_path in pdf_files:
        print(f"\nProcessing: {pdf_path.name}")

        reader = PdfReader(str(pdf_path))

        for page_number, page in enumerate(reader.pages, start=1):
            extracted_text = page.extract_text() or ""
            text = clean_text(extracted_text)

            if not text:
                print(
                    f"Warning: no extractable text on page {page_number}. "
                    "This page may need OCR."
                )
                continue

            for chunk_number, chunk in enumerate(
                split_into_chunks(text), start=1
            ):
                records.append(
                    {
                        "source": pdf_path.name,
                        "page": page_number,
                        "chunk_id": (
                            f"{pdf_path.stem}_p{page_number}_c{chunk_number}"
                        ),
                        "text": chunk,
                    }
                )

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_FILE.open("w", encoding="utf-8") as file:
        json.dump(records, file, ensure_ascii=False, indent=2)

    print("\nPDF ingestion completed.")
    print(f"PDF files processed: {len(pdf_files)}")
    print(f"Text chunks created: {len(records)}")
    print(f"Output saved to: {OUTPUT_FILE}")

    if not records:
        print(
            "Warning: no text was extracted. Check whether the PDF "
            "contains scanned pages requiring OCR."
        )


if __name__ == "__main__":
    main()

