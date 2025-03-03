from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import BadRequest
from app.models.tenant import Tenant


async def generate_tenant_verification_otp(db: AsyncSession, tenant: Tenant) -> str:
    """
    Generate & Save Tenant Verification OTP.
    """
    tenant.generate_otp()

    db.add(tenant)
    await db.commit()
    await db.refresh(tenant)

    return tenant.otp


async def validate_tenant_verification_otp(tenant: Tenant, otp: str) -> str:
    """
    Validate Tenant Verification OTP.
    """
    # Check if the OTP is invalid or expired
    if tenant.otp != otp or tenant.is_otp_expired():
        raise BadRequest("Invalid OTP")

    return "Valid OTP"
