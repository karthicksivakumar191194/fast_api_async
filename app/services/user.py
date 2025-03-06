from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import exists
from passlib.context import CryptContext

from app.models import Tenant, User, UserStatusEnum


# Create a password context using bcrypt hashing algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hashes the given password using a secure hashing algorithm.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies if the plain password matches the hashed password.
    """
    return pwd_context.verify(plain_password, hashed_password)


async def create_owner_user(db: AsyncSession, tenant: Tenant, name: str, email: str, password: str) -> User:
    """
    Creates a new owner user with the provided details.
    """
    user = User(
        tenant_id=tenant.id,
        name=name,
        email=email,
        password=hash_password(password),
        is_account_owner=True,
        status=UserStatusEnum.ACTIVE
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user


async def get_tenant_owner_user(db: AsyncSession, tenant: Tenant) -> User:
    """
    Get tenant owner user
    """
    result = await db.execute(select(User).filter(User.tenant_id == tenant.id, User.is_account_owner == True))
    user = result.scalars().first()

    return user


async def is_tenant_owner_email_exists(db: AsyncSession, email: str) -> bool:
    """
    Validate if tenant owner email exists
    """
    result = await db.execute(select(exists().where(User.email == email, User.is_account_owner == True)))
    user_exists = result.scalar()

    # TODO: If tenant deleted allow user to use this email

    return user_exists
