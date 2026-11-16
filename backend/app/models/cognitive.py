from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class CognitiveSession(Base):
    __tablename__ = "cognitive_sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    test_type: Mapped[str] = mapped_column(String(50))
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    sport_session_id: Mapped[int | None] = mapped_column(
        ForeignKey("sport_sessions.id", ondelete="SET NULL"), index=True
    )


class CognitiveTrial(Base):
    __tablename__ = "cognitive_trials"
    __table_args__ = (UniqueConstraint("cognitive_session_id", "trial_index"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    cognitive_session_id: Mapped[int] = mapped_column(
        ForeignKey("cognitive_sessions.id", ondelete="CASCADE"), index=True
    )
    trial_index: Mapped[int]
    reaction_time_ms: Mapped[int | None]
    is_premature: Mapped[bool] = mapped_column(default=False)