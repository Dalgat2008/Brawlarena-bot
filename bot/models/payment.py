import enum
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from bot.database import Base


class PaymentStatus(str, enum.Enum):
    pending = "pending"
    paid = "paid"
    failed = "failed"


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    amount: Mapped[float]
    asset: Mapped[str]
    status: Mapped[PaymentStatus] = mapped_column(default=PaymentStatus.pending)
    invoice_id: Mapped[str | None]