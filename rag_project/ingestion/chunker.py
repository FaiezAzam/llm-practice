
def chunk_text(
        text: str,
        chunk_size : int = 500,
        overlap : int = 100,
) -> list[str]:
      """
         Split text into chunks of roughly chunk_size characters,
         with overlap characters shared between consecutive chunks.
      """
      chunks = []
      step = chunk_size - overlap
      start = 0

      while start < len(text):
          chunk = text[start:start + chunk_size].strip()
          if chunk:
            chunks.append(chunk)
          start +=step

      if len(chunks) > 1 and len(chunks[-1]) < 50:
            chunks[-2] = chunks[-2] + " " + chunks[-1]
            chunks.pop()
      return chunks
    