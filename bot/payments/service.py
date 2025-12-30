from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from bot.models import User, Payment, PaymentStatus, Referral
from bot.payments.cryptobot import CryptoBotClient
from bot.config import settings


cryptobot = CryptoBotClient(settings.cryptobot_token)


class PaymentService:
    COMMISSION = 0.10
    REF_PERCENT = 0.30

    @staticmethod
    async def create_deposit(
        session: AsyncSession,
        user: User,
        amount: float,
    ):
        invoice = await cryptobot.create_invoice(amount)

        payment = Payment(
            user_id=user.id,
            amount=amount,
            asset=invoice["asset"],
            invoice_id=invoice["invoice_id"],
        )
        session.add(payment)
        await session.commit()

        return invoice["pay_url"]

    @staticmethod
    async def confirm_payment(
        session: AsyncSession,
        payment: Payment,
    ):
        payment.status = PaymentStatus.paid
        user = await session.get(User, payment.user_id)
        user.balance += payment.amount

        await session.commit()

    @staticmethod
    async def payout_winner(
        session: AsyncSession,
        user: User,
        amount: float,
    ):
        fee = amount * PaymentService.COMMISSION
        payout = amount - fee

        await cryptobot.transfer(
            user_id=user.telegram_id,
            amount=payout,
        )

        # рефералка
        ref = await session.scalar(
            select(Referral).where(Referral.referred_id == user.id)
        )
        if ref:
            ref_user = await session.get(User, ref.referrer_id)
            ref_user.balance += fee * PaymentService.REF_PERCENT

        await session.commit()