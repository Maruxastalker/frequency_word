from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class WordFrequency:
    lemma: str
    total_count: int = 0
    line_counts: Dict[int, int] = field(default_factory=dict)

    def increment(self, line_number: int) -> None:
        self.total_count += 1
        self.line_counts[line_number] = self.line_counts.get(line_number, 0) + 1 

    def  get_line_distribution(self, total_lines: str) -> List[int]:
        return [self.line_counts.get(i, 0) for i in range(total_lines)]

    def get_line_distribution_str(self, total_lines: int) -> str:
        """Получить распределение по строкам в виде строки '0,11,32,0,0,3'."""
        return ",".join(str(c) for c in self.get_line_distribution(total_lines))
    

@dataclass
class FrequencyReport:
    frequencies: Dict[str, WordFrequency] = field(default_factory=dict)
    total_lines: int = 0

    def add_word(self, lemma: str, line_number: int) -> None:
        if lemma not in self.frequencies:
            self.frequencies[lemma] = WordFrequency(lemma=lemma)
        self.frequencies[lemma].increment(line_number)

    def get_sorted_entries(self) -> List[WordFrequency]:
        return sorted(
            self.frequencies.values(),
            key= lambda wf: wf.total_count,
            reverse=True
        )