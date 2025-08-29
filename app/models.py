from dataclasses import dataclass, asdict, field
from typing import List
from datetime import datetime
import uuid

def now_str():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@dataclass
class Entry:
    id: str
    word: str
    phonetic: str = ""
    meaning: str = ""
    topic: str = ""
    example: str = ""
    phrases: List[str] = field(default_factory=list)  # "实用短语/固定搭配"
    familiarity: int = 1  # 1~5
    notes: str = ""
    created_at: str = ""
    updated_at: str = ""

    @staticmethod
    def create(
        word: str,
        phonetic: str = "",
        meaning: str = "",
        topic: str = "",
        example: str = "",
        phrases=None,
        familiarity: int = 1,
        notes: str = "",
    ) -> "Entry":
        phrases = phrases or []
        _id = str(uuid.uuid4())
        ts = now_str()
        return Entry(
            id=_id,
            word=word.strip(),
            phonetic=phonetic.strip(),
            meaning=meaning.strip(),
            topic=topic.strip(),
            example=example.strip(),
            phrases=[p.strip() for p in phrases if p.strip()],
            familiarity=int(familiarity) if str(familiarity).isdigit() else 1,
            notes=notes.strip(),
            created_at=ts,
            updated_at=ts,
        )

    def to_dict(self):
        return asdict(self)
