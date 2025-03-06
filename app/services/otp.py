from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta

from app.models.user import User


async def generate_user_otp(db: AsyncSession, user: User) -> str:
    """
    Generate & Save User OTP.
    """
    user.generate_otp()

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user.otp

async def get_or_generate_user_otp(db: AsyncSession, user: User) -> str:
    """
    Get or Generate & Save User OTP.

    If OTP resend request received before 5 minutes, send old OTP
    If OTP resend request received after 5 minutes, generate new OTP
    """
    otp_valid_till = datetime.utcnow() + timedelta(minutes=5)

    if not otp_valid_till > user.otp_expiry_at:
        user.generate_otp()
        db.add(user)
        await db.commit()
        await db.refresh(user)

    return user.otp
