from typing import Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import User
from app.exceptions import ValidationError


async def _validate_owner_email(db: AsyncSession, email: str, errors: Dict):
    result = await db.execute(select(User).filter(User.email == email, User.is_account_owner))
    user = result.scalars().first()

    # TODO: If tenant deleted allow user to use this email

    if user:
        errors["owner_email"] = "Email already exists"


async def validate_onboard_request(db: AsyncSession, request):
    errors = {}

    # Validate owner email
    await _validate_owner_email(db, request.owner_email, errors)

    # If there are errors, raise a ValidationError with all errors
    if errors:
        raise ValidationError(detail=errors)
