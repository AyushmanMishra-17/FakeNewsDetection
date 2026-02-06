import PyPDF2
def parse_file(file):
    if file.filename.endswith(".txt"):
        return file.file.read().decode()
    if file.filename.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file.file)
        return "".join(p.extract_text() for p in reader.pages)
    return ""