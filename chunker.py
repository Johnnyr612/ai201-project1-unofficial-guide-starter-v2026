"""
Stage 2 of the pipeline: splitting documents into chunks.

⚠️ THIS IS THE FILE YOU CHANGE IN MILESTONE 3.

`split_documents` below is deliberately plain. It cuts every document into
fixed-size pieces with a fixed overlap and pays no attention to where sentences
or paragraphs end. It works, and it is not good.

On a corpus of short posts it may not cut anything at all: `campus_life` comes
out as 88 documents and 88 chunks, because almost nothing in it reaches 800
characters. That is the baseline, not a bug — Milestone 3 is where you decide
whether one post should stay one chunk.

Your job in Milestone 3 is to replace the *body* of `split_documents` with a
strategy that fits the documents you actually read in Milestone 1. Keep the
name and the shape of what it returns — the rest of the pipeline calls it, and
your README has to name the function that produced your chunks.

If you get stuck for 30 minutes, `fallback_split` is the original. Switch back
to it, write down what you saw, and move on. That's a real observation about
your pipeline, not giving up.
"""

import re
from dataclasses import dataclass

import config
from ingest import Document


@dataclass
class Chunk:
    """One piece of one document."""

    text: str
    source: str        # which file it came from
    index: int         # which chunk within that file, starting at 0
    produced_by: str   # the function that made it — cite this in your README

    @property
    def label(self) -> str:
        return f"{self.source}#{self.index}"


def fallback_split(
    documents: list[Document],
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[Chunk]:
    """
    The starter's original chunker. Fixed-size character windows with overlap.

    Keep this function. Milestone 3's stop rule points back at it, and having
    something to compare your own strategy against is useful in unit 2.
    """
    chunk_size = chunk_size or config.CHUNK_SIZE
    overlap = overlap or config.CHUNK_OVERLAP

    if overlap >= chunk_size:
        raise ValueError("overlap has to be smaller than chunk_size")

    chunks: list[Chunk] = []
    for doc in documents:
        start = 0
        index = 0
        while start < len(doc.text):
            piece = doc.text[start : start + chunk_size].strip()
            if piece:
                chunks.append(
                    Chunk(
                        text=piece,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::fallback_split",
                    )
                )
                index += 1
            start += chunk_size - overlap

    return chunks


def split_documents(documents: list[Document]) -> list[Chunk]:
    """Chunk long, structured documents by sections and paragraphs.

    `city_guides` is built around headings and paragraphs, not arbitrary character
    windows. This strategy keeps each labelled section together when possible and
    only splits a section when it grows too large.
    """
    target_size = 650
    overlap_size = 0
    chunks: list[Chunk] = []

    def sentence_chunks(text: str) -> list[str]:
        text = text.strip()
        if not text:
            return []
        if len(text) <= target_size:
            return [text]

        sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
        if not sentences:
            return [text]

        out: list[str] = []
        current = ""
        for sentence in sentences:
            candidate = f"{current} {sentence}".strip()
            if len(candidate) <= target_size:
                current = candidate
            else:
                if current:
                    out.append(current)
                if len(sentence) > target_size:
                    # Very long sentences should still be broken up without losing meaning.
                    for i in range(0, len(sentence), target_size):
                        piece = sentence[i : i + target_size].strip()
                        if piece:
                            out.append(piece)
                    current = ""
                else:
                    current = sentence
        if current:
            out.append(current)
        return out

    def finalize_block(block: str, index_start: int) -> None:
        nonlocal chunks
        if not block.strip():
            return
        parts = sentence_chunks(block)
        for i, part in enumerate(parts):
            idx = index_start + i
            chunks.append(
                Chunk(
                    text=part.strip(),
                    source=doc.source,
                    index=idx,
                    produced_by="chunker.py::split_documents",
                )
            )

    for doc in documents:
        blocks = [b.strip() for b in re.split(r"\n\s*\n+", doc.text.strip()) if b.strip()]

        if not blocks:
            continue

        current: list[str] = []
        current_len = 0
        doc_index = 0

        for block in blocks:
            block_text = block.strip()
            if block_text.startswith("#"):
                if current:
                    buffer = "\n\n".join(current)
                    for part in sentence_chunks(buffer):
                        chunks.append(
                            Chunk(
                                text=part.strip(),
                                source=doc.source,
                                index=doc_index,
                                produced_by="chunker.py::split_documents",
                            )
                        )
                        doc_index += 1
                    current = []
                    current_len = 0
                current.append(block_text)
                current_len = len(block_text)
                continue

            candidate = "\n\n".join(current + [block_text]) if current else block_text
            if len(candidate) <= target_size:
                current.append(block_text)
                current_len = len(candidate)
                continue

            if current:
                buffer = "\n\n".join(current)
                for part in sentence_chunks(buffer):
                    chunks.append(
                        Chunk(
                            text=part.strip(),
                            source=doc.source,
                            index=doc_index,
                            produced_by="chunker.py::split_documents",
                        )
                    )
                    doc_index += 1
                current = []
                current_len = 0

            # If a single paragraph is too long, split it into sentence-size chunks.
            for part in sentence_chunks(block_text):
                chunks.append(
                    Chunk(
                        text=part.strip(),
                        source=doc.source,
                        index=doc_index,
                        produced_by="chunker.py::split_documents",
                    )
                )
                doc_index += 1

        if current:
            buffer = "\n\n".join(current)
            for part in sentence_chunks(buffer):
                chunks.append(
                    Chunk(
                        text=part.strip(),
                        source=doc.source,
                        index=doc_index,
                        produced_by="chunker.py::split_documents",
                    )
                )
                doc_index += 1

    # Deliberately keep overlap at 0 for city guides: the documents are already
    # sectioned, and a small repeat across boundary lines was creating fragmentary
    # chunks that merged unrelated material instead of preserving useful context.
    return chunks


def describe(chunks: list[Chunk]) -> str:
    """A one-line summary, printed after indexing."""
    if not chunks:
        return "0 chunks"
    lengths = [len(c.text) for c in chunks]
    return (
        f"{len(chunks)} chunks, "
        f"{sum(lengths) // len(lengths)} characters on average "
        f"(shortest {min(lengths)}, longest {max(lengths)}), "
        f"produced by {chunks[0].produced_by}"
    )


if __name__ == "__main__":
    from ingest import load_documents

    chunks = split_documents(load_documents())
    print(describe(chunks))
