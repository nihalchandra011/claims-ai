# backend/parsers.py

import io
import tempfile
from x12_edi_tools.x12_parser import X12Parser

import pandas as pd
import pdfplumber
from docx import Document
from PIL import Image
import pytesseract

# ---------- Generic text extraction ----------

def parse_txt(file_bytes: bytes) -> str:
    return file_bytes.decode("utf-8", errors="ignore")

def parse_csv(file_bytes: bytes) -> str:
    df = pd.read_csv(io.BytesIO(file_bytes))
    return df.to_string(index=False)

def parse_xlsx(file_bytes: bytes) -> str:
    df = pd.read_excel(io.BytesIO(file_bytes))
    return df.to_string(index=False)

def parse_pdf(file_bytes: bytes) -> str:
    text_parts = []
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""
            text_parts.append(text)
    return "\n".join(text_parts)

def parse_docx(file_bytes: bytes) -> str:
    doc = Document(io.BytesIO(file_bytes))
    return "\n".join(p.text for p in doc.paragraphs if p.text)

# Replace this with the actual install path on your system
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def parse_image(file_bytes: bytes) -> str:
    img = Image.open(io.BytesIO(file_bytes))
    return pytesseract.image_to_string(img)

def parse_any(filename: str, file_bytes: bytes) -> str:
    fn = filename.lower()
    if fn.endswith(".txt") or fn.endswith(".dat"):
        return parse_txt(file_bytes)
    if fn.endswith(".csv"):
        return parse_csv(file_bytes)
    if fn.endswith(".xlsx"):
        return parse_xlsx(file_bytes)
    if fn.endswith(".pdf"):
        return parse_pdf(file_bytes)
    if fn.endswith(".docx"):
        return parse_docx(file_bytes)
    if fn.endswith((".png", ".jpg", ".jpeg")):
        return parse_image(file_bytes)
    raise ValueError(f"Unsupported file type: {filename}")

# ---------- X12 normalization + parsing ----------

def normalize_x12_text(raw_bytes: bytes) -> str:
    text = raw_bytes.decode("latin-1", errors="ignore")
    isa_pos = text.find("ISA")
    if isa_pos == -1:
        raise ValueError("No ISA segment found.")
    text = text[isa_pos:]
    if len(text) < 107:
        raise ValueError("EDI too short to detect delimiters.")
    segment_terminator = text[106]
    text = text.replace("\r\n", segment_terminator)\
               .replace("\n", segment_terminator)\
               .replace("\r", segment_terminator)
    while segment_terminator * 2 in text:
        text = text.replace(segment_terminator*2, segment_terminator)
    return text

def parse_x12_bytes(file_bytes: bytes) -> dict:
    clean_text = normalize_x12_text(file_bytes)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".edi") as tmp:
        tmp.write(clean_text.encode("latin-1"))
        tmp_path = tmp.name
    parser = X12Parser()
    parsed = parser.parse(tmp_path)
    return parsed