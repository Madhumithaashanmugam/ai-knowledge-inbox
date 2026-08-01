def create_chunks(
    text: str,
    chunk_size: int = 1000,
    overlap: int = 200
):
    """
    Split text into overlapping chunks.

    - chunk_size: Maximum characters per chunk.
    - overlap: Characters shared between consecutive chunks.
    """

    if not text.strip():
        return []

    text = " ".join(text.split())

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:

        end = start + chunk_size

        if end < text_length:
            last_space = text.rfind(" ", start, end)

            if last_space != -1:
                end = last_space

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start = end - overlap

        if start < 0:
            start = 0

    return chunks