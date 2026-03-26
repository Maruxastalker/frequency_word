import asyncio

from fastapi import UploadFile

from app.domain.services.frequency_analyzer import FrequencyAnalyzer
from app.infrastucture.file_reader import FileReader
from app.infrastucture.excel_writer import ExcelReportWriter


class ReportExportService:

    def __init__(self) -> None:
        self._file_reader = FileReader()
        self._analyzer = FrequencyAnalyzer()
        self._writer = ExcelReportWriter()

    async def export(self, upload: UploadFile) -> str:

        lines = self._file_reader.read_lines(upload)
        report = await self._analyzer.analyzer(lines)

        loop = asyncio.get_event_loop()
        file_path = await loop.run_in_executor(None, self._writer.write, report)

        return file_path