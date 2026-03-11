"""
Инфраструктурный сервис чтения файлов.
"""

import codecs
from typing import AsyncIterator

from fastapi import UploadFile, HTTPException


class FileReader:
    """Потоковое чтение загруженных файлов."""

    def __init__(self, chunk_size: int = 1024 * 1024):
        self._chunk_size = chunk_size

    async def read_lines(self, upload: UploadFile) -> AsyncIterator[str]:
        """
        Читает UploadFile построчно.
        Использует инкрементальный декодер для корректной
        обработки многобайтовых символов на границах чанков.
        """
        decoder = codecs.getincrementaldecoder("utf-8")(errors="strict")
        buffer = ""

        try:
            while True:
                chunk_bytes = await upload.read(self._chunk_size)

                if not chunk_bytes:
                    buffer += decoder.decode(b"", final=True)
                    break

                buffer += decoder.decode(chunk_bytes, final=False)

                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    yield line

        except UnicodeDecodeError:
            raise HTTPException(
                status_code=400,
                detail="Файл должен быть в кодировке UTF-8."
            )

        if buffer:
            yield buffer