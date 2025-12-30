from sqlalchemy import (
    BigInteger,
    String,
    Integer,
    Boolean,
    ForeignKey,
    DateTime,
    Enum,
    Numeric,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from bot.database import Base


# ===== ENUMS =====

class MatchStatus(enum.Enum):
    waiting = "waiting"
    active = "active"
    finished = "finished"
    cancelled = "cancelled"
    error = "error"


class MatchMode(enum.Enum):
    solo = "solo"
    duel = "duel"


class PaymentStatus(enum.Enum):
    pending = "pending"
    paid = "paid"
    failed = "failed"


# ===== MODELS =====

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    username: Mapped[str | None] = mapped_column(String(64))

    nickname: Mapped[str] = mapped_column(String(64))
    player_tag: Mapped[str] = mapped_column(String(32), unique=True)

    balance: Mapped[float] = mapped_column(Numeric(12, 2), default=0)

    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    is_banned: Mapped[bool] = mapped_column(Boolean, default=False)

    referral_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # relations
    referrals = relationship("User", remote_side=[id])
    matches = relationship("Match", secondary="match_players")


class Match(Base):
    __tablename__ = "matches"

    id: Mapped[int] = mapped_column(primary_key=True)

    mode: Mapped[MatchMode] = mapped_column(Enum(MatchMode))
    status: Mapped[MatchStatus] = mapped_column(Enum(MatchStatus), default=MatchStatus.waiting)

    max_players: Mapped[int] = mapped_column(Integer)
    lobby_code: Mapped[str | None] = mapped_column(String(128))

    started_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True))
    finished_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True))

    winner_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    players = relationship("User", secondary="match_players")


class MatchPlayer(Base):
    __tablename__ = "match_players"

    match_id: Mapped[int] = mapped_column(
        ForeignKey("matches.id"), primary_key=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), primary_key=True
    )


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    amount: Mapped[float] = mapped_column(Numeric(12, 2))
    status: Mapped[PaymentStatus] = mapped_column(
        Enum(PaymentStatus), default=PaymentStatus.pending
    )

    invoice_id: Mapped[str] = mapped_column(String(128), unique=True)

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class ReferralEarning(Base):
    __tablename__ = "referral_earnings"

    id: Mapped[int] = mapped_column(primary_key=True)
    referrer_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    referred_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    amount: Mapped[float] = mapped_column(Numeric(12, 2))

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )