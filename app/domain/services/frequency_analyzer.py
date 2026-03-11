import asyncio
from typing import AsyncIterator

from app.domain.models.word_frequency import FrequencyReport
from app.domain.services.lemmatizer import Lemmatizer

class FrequencyAnalyzer:

    def __init__(self) -> None:
        self._lemmatizer = Lemmatizer()

    async def analyzer(self, lines: AsyncIterator[str]) -> FrequencyReport:

        report = FrequencyReport()
        line_number = 0
        loop = asyncio.get_event_loop()

        async for line in lines:
            lemmas = await loop.run_in_executor(
                None,
                self._lemmatizer.extract_and_lematize,
                line
            )


            for lemma in lemmas:
                report.add_word(lemma, line_number)
            line_number += 1

        report.total_lines = line_number
        return report

