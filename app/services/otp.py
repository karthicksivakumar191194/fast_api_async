from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import BadRequest
from app.models.user import User


async def generate_user_verification_otp(db: AsyncSession, user: User) -> str:
    """
    Generate & Save User Verification OTP.
    """
    user.generate_otp()

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user.otp


async def validate_tenant_verification_otp(user: User, otp: str) -> str:
    """
    Validate User Verification OTP.
    """
    # Check if the OTP is invalid or expired
    if user.otp != otp or user.is_otp_expired():
        raise BadRequest("Invalid OTP")

    return "Valid OTP"
