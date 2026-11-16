from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class SportSession(Base):
    __tablename__ = "sport_sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    sport: Mapped[str] = mapped_column(String(20))
    played_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    focus_rating: Mapped[int]
    fatigue_rating: Mapped[int]
    notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class GolfPerformance(Base):
    __tablename__ = "golf_performance"

    sport_session_id: Mapped[int] = mapped_column(
        ForeignKey("sport_sessions.id", ondelete="CASCADE"), primary_key=True
    )
    holes_played: Mapped[int]
    total_strokes: Mapped[int]
    course_par: Mapped[int]
    fairways_hit: Mapped[int]
    fairways_attempted: Mapped[int]
    greens_in_regulation: Mapped[int]
    total_putts: Mapped[int]


class VolleyballPerformance(Base):
    __tablename__ = "volleyball_performance"

    sport_session_id: Mapped[int] = mapped_column(
        ForeignKey("sport_sessions.id", ondelete="CASCADE"), primary_key=True
    )
    sets_played: Mapped[int]
    serves_attempted: Mapped[int]
    service_errors: Mapped[int]
    aces: Mapped[int]
    attack_attempts: Mapped[int]
    kills: Mapped[int]
    attack_errors: Mapped[int]
    digs: Mapped[int]