from rag_project.ingestion.chunker import chunk_text

# Build a unique string: "line 1 ", "line 2 ", "line 3 ", ...
text = " ".join(f"line-{i}" for i in range(1, 201))

chunks = chunk_text(text, chunk_size=200, overlap=50)

print(f"Total chunks: {len(chunks)}")
print()
for i, chunk in enumerate(chunks):
    
    print(f"Chunk {i}: length={len(chunk)}")
    print(f"  starts with: {chunk[:60]!r}")
    print(f"  ends with:   {chunk[-60:]!r}")
    print()