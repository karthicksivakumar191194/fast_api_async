from typing import Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import User, UserIdentifierType, UserStatusEnum, Tenant, TenantStatusEnum
from app.exceptions import ValidationError, BadRequest
from app.services.user import verify_password


async def _validate_username(db: AsyncSession, username: str, user_identifier_type: UserIdentifierType, errors: Dict):
    """
    Validate username(email address or mobile no)
    """
    if user_identifier_type == "email":
        users = await db.execute(select(User).filter(User.email == username, User.status == UserStatusEnum.ACTIVE))
        error_message = "Invalid email"
    else:
        users = await db.execute(select(User).filter(User.phone_number == username, User.status == UserStatusEnum.ACTIVE))
        error_message = "Invalid mobile no"

    users = users.unique().scalars().all()

    if not users:
        errors["username"] = error_message

    return users


async def _validate_tenant(db: AsyncSession, tenant_id: str) -> Tenant:
    """
    Validate tenant
    """
    tenant = await db.execute(select(Tenant).filter(Tenant.id == tenant_id,
                                                    Tenant.status == TenantStatusEnum.ACTIVE))

    tenant = tenant.scalars().first()

    if tenant:
         # If the tenant status not active throw error
        if tenant.status != TenantStatusEnum.ACTIVE:
            raise BadRequest(detail="You don't have access to the application")
    else:
        raise BadRequest(detail="Invalid credentials")

    return tenant


async def _validate_user(db: AsyncSession, tenant_id: str, username: str,
                                     user_identifier_type: UserIdentifierType):
    """
    Validate user account
    """
    if user_identifier_type == "email":
        user = await db.execute(select(User).filter(User.tenant_id == tenant_id, User.email == username))
    else:
        user = await db.execute(select(User).filter(User.tenant_id == tenant_id, User.phone_number == username))

    user = user.scalars().first()

    if user:
        # If the user status not active throw error
        if user.status == UserStatusEnum.DELETED:
            raise BadRequest(detail="You don't have access to the application")
        elif user.status == UserStatusEnum.INACTIVE:
            raise BadRequest(detail="Your account is inactive. Please contact the admin.")
        elif user.status == UserStatusEnum.NOT_VERIFIED:
            raise BadRequest(detail="Your account has not been verified yet")
    else:
        raise BadRequest(detail="Invalid credentials")


async def validate_username(db: AsyncSession, username: str, user_identifier_type: UserIdentifierType):
    """
    Validate username(email address or mobile no)

    used on: login with username(email address or mobile no) API
    """
    errors = {}

    # validate username(email address or mobile no)
    users = await _validate_username(db, username, user_identifier_type, errors)

    # If there are errors, raise a ValidationError with all errors
    if errors:
        raise ValidationError(detail=errors)

    return users

async def validate_login_credentials(db: AsyncSession, tenant_id: str, username: str,
                                     user_identifier_type: UserIdentifierType, password: str) -> User:
    """
    Validate Login Credentials

    used on: login with password API
    """
    # Validate tenant
    await _validate_tenant(db, tenant_id)

    # Validate user
    user = await _validate_user(db, tenant_id, username, user_identifier_type)

    if not verify_password(user.password, password):
        raise BadRequest("Invalid credentials. Incorrect password.")

    return user


async def validate_otp_request(db: AsyncSession, tenant_id: str, username: str,
                                     user_identifier_type: UserIdentifierType) -> User:
    """
    Validate OTP Request

    used on: request OTP & verify OTP API
    """
    # Validate tenant
    await _validate_tenant(db, tenant_id)

    # Validate user
    user = await _validate_user(db, tenant_id, username, user_identifier_type)

    return user


async def validate_user_otp(user: User, otp: str) -> str:
    """
    Validate User OTP.

    used on: verify OTP API
    """
    # Check if the OTP is invalid or expired
    if user.otp != otp or user.is_otp_expired():
        raise BadRequest("Invalid OTP")

    return "Valid OTP"