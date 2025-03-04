import asyncio
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Form, APIRouter, BackgroundTasks, Depends, status

from app.db.database import get_db
from app.services.tenant import create_tenant
from app.services.user import create_owner_user
from app.services.otp import generate_user_verification_otp
from app.services.email import send_account_verification_otp
from app.services.gsheet import add_tenant_details_to_admin_gsheet, update_tenant_details_to_admin_gsheet
from app.schemas.onboarding import OnboardRequest, OnboardResponse
from app.validators.onboarding import validate_onboard_request


router = APIRouter()

@router.post("/", response_model=OnboardResponse, status_code=status.HTTP_201_CREATED)
async def onboard_tenant(
    request:  Annotated[OnboardRequest, Form()],
    background_tasks: BackgroundTasks,
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
    user = await create_owner_user(db, tenant, request.owner_name, request.owner_email, request.owner_password)

    # Generate User Verification OTP
    otp = await generate_user_verification_otp(db, user)

    # Send Account Verification OTP to Owner Email & Sync Tenant Details to Google Sheets
    # await asyncio.gather(
    #     send_account_verification_otp(otp, request.owner_email),
    #     add_tenant_details_to_admin_gsheet(tenant, request.owner_name, request.owner_email)
    # )

    background_tasks.add_task(send_account_verification_otp, otp, request.owner_email)
    background_tasks.add_task(add_tenant_details_to_admin_gsheet, tenant, request.owner_name, request.owner_email)

    return OnboardResponse(
        message="Account has been created successfully. Use the OTP from the email to proceed."
    )


@router.post("/otp/verify", status_code=status.HTTP_200_OK)
async def verify_otp(request):
    """
    Endpoint to verify the OTP (One Time Password) for the user.
    """

    # TODO Functionality

    return {
        "message": "OTP verified, login successful"
    }


@router.post("/otp/resend", status_code=status.HTTP_200_OK)
async def resend_otp(request):
    """
    Endpoint to resend an OTP (One Time Password) to the user.
    """

    # TODO Functionality

    return {
        "message": "OTP resent successfully"
    }


@router.post("/company-information", status_code=status.HTTP_200_OK)
async def save_company_information(request):
    """
    Endpoint to save company information
    """

    # TODO Functionality

    return OnboardResponse(message="Success")


@router.post("/finish", status_code=status.HTTP_200_OK)
async def finish(request, background_tasks: BackgroundTasks,):
    """
    Endpoint to complete the tenant setup, creating default workspace, default location, default team,
    and default roles.
    Tenant will be updated to status "Active".
    """
    tenant = ""

    # TODO Functionality

    background_tasks.add_task(update_tenant_details_to_admin_gsheet, tenant)

    return OnboardResponse(message="Success")