from typing import ClassVar

import tiktoken

from haiku.rag.config import Config


class Chunker(object):

    encoder: ClassVar[tiktoken.Encoding] = tiktoken.encoding_for_model("gpt-3.5-turbo")

    def __init__(
        self,
        chunk_size: int = Config.CHUNK_SIZE,
        chunk_overlap: int = Config.CHUNK_OVERLAP,
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    async def chunk(self, text: str) -> list[str]:
        encoded_tokens = self.encoder.encode(text, disallowed_special=())

        if self.chunk_size > len(encoded_tokens):
            return [text]

        chunks = []
        i = 0
        split_id_counter = 0
        while i < len(encoded_tokens):
            # Overlap
            start_i = i
            end_i = min(i + self.chunk_size, len(encoded_tokens))

            chunk_tokens = encoded_tokens[start_i:end_i]
            chunk_text = self.encoder.decode(chunk_tokens)

            chunks.append(chunk_text)
            split_id_counter += 1

            # Exit loop if this was the last possible chunk
            if end_i == len(encoded_tokens):
                break

            i += (
                self.chunk_size - self.chunk_overlap
            )  # Step forward, considering overlap
        return chunks


chunker = Chunker()
