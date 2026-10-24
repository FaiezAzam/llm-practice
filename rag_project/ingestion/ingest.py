from pathlib import Path
from rag_project.ingestion.pdf_loader import load_pdf
from rag_project.ingestion.chunker import chunk_text

def ingest_documents(folder: str) -> list[dict]:
    chunks = []
    pdf_files = Path(folder).glob("*.pdf")

    for pdf_path in pdf_files:
        pages = load_pdf(str(pdf_path))
        for page in pages:
            page_chunks = chunk_text(page["text"])
            for chunk in page_chunks:
                chunks.append({
                    "text": chunk,
                    "source": pdf_path.name,
                    "page": page["page"],
                    "chunk_index": len(chunks),
                })
    return chunks

if __name__ == "__main__":
    import json

    chunks = ingest_documents("rag_project/data/documents")
    print(f"Total chunks: {len(chunks)}")

    for chunk in chunks[:2]:
        print(chunk)
        print("---")

    with open("rag_project/data/chunks.json", "w") as f:
         json.dump(chunks, f, indent=2)
    print("Saved to rag_project/data/chunks.json")


        