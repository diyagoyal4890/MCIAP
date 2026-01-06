import os
import json
import csv

# Optional imports (PDF / DOCX ke liye)
try:
    import docx
except:
    docx = None

try:
    import PyPDF2
except:
    PyPDF2 = None


def read_file(file_path):
    """
    Reads content from different file formats and returns text
    """
    ext = os.path.splitext(file_path)[1].lower()

    try:
        # ---------- TXT ----------
        if ext == ".txt":
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()

        # ---------- CSV ----------
        elif ext == ".csv":
            text = ""
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                reader = csv.reader(f)
                for row in reader:
                    text += " ".join(row) + "\n"
            return text

        # ---------- JSON ----------
        elif ext == ".json":
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                data = json.load(f)
                return json.dumps(data, ensure_ascii=False)

        # ---------- XML ----------
        elif ext == ".xml":
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()

        # ---------- PDF ----------
        elif ext == ".pdf" and PyPDF2:
            text = ""
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text += page.extract_text() or ""
            return text

        # ---------- DOCX ----------
        elif ext == ".docx" and docx:
            document = docx.Document(file_path)
            return "\n".join([p.text for p in document.paragraphs])

    except Exception as e:
        print("File read error:", e)

    return ""