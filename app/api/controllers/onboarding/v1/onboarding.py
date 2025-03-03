import asyncio
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Form, APIRouter, Depends, status

from app.settings import settings
from app.db.database import get_db
from app.services.tenant import create_tenant
from app.services.user import create_owner_user
from app.services.otp import generate_tenant_verification_otp
from app.services.email import send_account_verification_otp
from app.services.gsheet import add_tenant_details_to_admin_gsheet
from app.schemas.onboarding import OnboardRequest, OnboardResponse
from app.validators.onboarding import validate_onboard_request


router = APIRouter()

@router.post("/", response_model=OnboardResponse, status_code=status.HTTP_201_CREATED)
async def onboard_tenant(
    request:  Annotated[OnboardRequest, Form()],
    db: AsyncSession = Depends(get_db)
) -> OnboardResponse:
    """
    Endpoint to onboard a new tenant, along with creating an owner account.
    Tenant will be in status "Not Verified" once onboarded.
    The owner will receive an OTP in email for verification after the onboarding is complete.
    """
    # Validate the request before proceeding to the business logic
    await validate_onboard_request(db, request)

    # Create Tenant
    tenant = await create_tenant(
        db,
        False,
        request.company_name
    )

    # Create Owner User
    await create_owner_user(db, tenant, request.owner_name, request.owner_email, request.owner_password)

    # Generate Tenant Verification OTP
    otp = await generate_tenant_verification_otp(db, tenant)

    # Send Account Verification OTP to Owner Email & Sync Tenant Details to Google Sheets
    await asyncio.gather(
        send_account_verification_otp(otp, request.owner_email),
        add_tenant_details_to_admin_gsheet(settings.environment)
    )

    return OnboardResponse(
        message="Account has been created successfully. Use the OTP from the email to proceed."
    )
