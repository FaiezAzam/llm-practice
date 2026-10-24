from pypdf import PdfReader

def load_pdf(file_path: str) -> list[dict]:
    """
     Load a pdf file and return a list of pages.
     Each item is a dict with 'text' and 'page' keys
    """
    reader = PdfReader(file_path)
    result = []
    for page_num,page in enumerate(reader.pages, start = 1):
        text = page.extract_text()
        if not text.strip():
            continue   
        result.append({"text": text, "page": page_num}) 

    return result



    