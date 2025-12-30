import enum
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from bot.database import Base


class MatchMode(str, enum.Enum):
    solo = "solo"
    duel = "duel"


class MatchStatus(str, enum.Enum):
    waiting = "waiting"
    started = "started"
    finished = "finished"
    canceled = "canceled"


class Match(Base):
    __tablename__ = "matches"

    id: Mapped[int] = mapped_column(primary_key=True)
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    mode: Mapped[MatchMode]
    max_players: Mapped[int]
    status: Mapped[MatchStatus] = mapped_column(default=MatchStatus.waiting)
    lobby_code: Mapped[str | None]
    winner_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))