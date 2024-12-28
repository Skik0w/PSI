from datetime import datetime
from asyncpg import Record  # type: ignore
from pydantic import BaseModel, ConfigDict, UUID4
from typing import Optional

from quizapi.infrastructure.dto.quizdto import QuizDTO


class HistoryDTO(BaseModel):
    id: int
    player_id: UUID4
    quiz: QuizDTO
    total_questions: int
    correct_answers: Optional[int]
    effectiveness: Optional[float]
    timestamp: datetime

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )

    @classmethod
    def from_record(cls, record: Record) -> "HistoryDTO":
        record_dict = dict(record)
        return cls(
            id=record_dict.get("id"),
            player_id=record_dict.get("player_id"),
            quiz=QuizDTO(
                id=record_dict.get("quiz_id"),
                title=record_dict.get("title"),
                player_id=record_dict.get("player_id_2"),
                description=record_dict.get("description"),
                shared=record_dict.get("shared"),
            ),
            total_questions=record_dict.get("total_questions"),
            correct_answers=record_dict.get("correct_answers"),
            effectiveness=record_dict.get("effectiveness"),
            timestamp=record_dict.get("timestamp"),
        )
