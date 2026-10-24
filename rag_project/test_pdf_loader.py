from rag_project.ingestion.pdf_loader import load_pdf
pages = load_pdf("rag_project/data/documents/html_tutorial.pdf")
print(f"Total pages with text:{len(pages)}")
print(f"first page no:{pages[0]['page']}")
print(f"first 300 characters:\n{pages[0]['text'][:300]}")