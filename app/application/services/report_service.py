import asyncio

from fastapi import UploadFile

from app.domain.services.frequency_analyzer import FrequencyAnalyzer
from app.infrastucture.file_reader import FileReader
from app.infrastucture.excel_writer import ExcelReportWriter


class ReportExportService:
    """
    Use-case: принять файл → частотный анализ → Excel.
    
    CPU-bound операции выполняются через run_in_executor,
    чтобы не блокировать event loop.
    """

    def __init__(self) -> None:
        self._file_reader = FileReader()
        self._analyzer = FrequencyAnalyzer()
        self._writer = ExcelReportWriter()

    async def export(self, upload: UploadFile) -> str:
        """
        Основной сценарий экспорта.
        
        Returns:
            Путь к сгенерированному xlsx-файлу.
        """
        # Шаг 1: читаем файл и анализируем
        lines = self._file_reader.read_lines(upload)
        report = await self._analyzer.analyzer(lines)

        # Шаг 2: записываем Excel (CPU-bound → executor)
        loop = asyncio.get_event_loop()
        file_path = await loop.run_in_executor(None, self._writer.write, report)

        return file_path