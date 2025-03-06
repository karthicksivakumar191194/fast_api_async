from typing import Annotated
from fastapi import Form, APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.models import UserIdentifierType
from app.schemas.base_schema import Response
from app.schemas.login import UserTenantListResponse, LoginRequest, LoginResponse, OTPLoginRequest, OTPVerifyRequest
from app.services.otp import generate_user_otp, get_or_generate_user_otp
from app.services.workspace import get_default_workspace_id
from app.validators.login import validate_username, validate_login_credentials, validate_otp_request, validate_user_otp

router = APIRouter()

# Step 1: User enters email or mobile number
@router.get("/", response_model=UserTenantListResponse, status_code=status.HTTP_200_OK)
async def login_with_email_or_mobile(username: str, user_identifier_type: UserIdentifierType,
                                     db: AsyncSession = Depends(get_db)):
    """
    Endpoint to retrieve active user accounts based on email address or mobile number.

    This endpoint checks the status of user profile associated with the provided
    email address or mobile number. For each active user profile found, it checks if
    the associated tenant is active. If the tenant is active, it returns the
    tenant's details along with the associated user account information.
    """
    # Validate username(email address or mobile no)
    users = await validate_username(db, username, user_identifier_type)

    user_data = [
        UserTenantListResponse(
            tenant_id=str(user.tenant.id),
            tenant_domain=user.tenant.domain or '',
            company_name=user.tenant.company_name or '',
            company_logo=user.tenant.company_logo or '',
            user_id=str(user.id),
            user_name=user.name,
            user_image=user.image or '',
        )
        for user in users
    ]

    return { "data": user_data }


# Step 2-A: User enters password
@router.post("/password", response_model=LoginResponse, status_code=status.HTTP_200_OK)
async def login_with_password(request: Annotated[LoginRequest, Form()],db: AsyncSession = Depends(get_db)):
    """
    Endpoint to validate the email address or mobile number and password for the selected tenant(account).

    This endpoint checks if both the user profile & selected tenant(account) is active.
    """
    # Validate login credentials
    user = await validate_login_credentials(db,
                                             request.tenant_id,
                                             request.username,
                                             request.user_identifier_type,
                                             request.password)

    default_workspace_id = await get_default_workspace_id(request.tenant_id)

    # TODO
    return {
        "data": {"tenant_id": "", "user_id": "", "user_name": "", "user_image": "", "default_workspace_id": ""},
        "message": "Logged in successfully"
    }


# Step 2-B-1: User requests OTP for login
@router.post("/otp", response_model=Response, status_code=status.HTTP_200_OK)
async def request_otp(request: Annotated[OTPLoginRequest, Form()],db: AsyncSession = Depends(get_db)):
    """
    Endpoint to request an OTP (One Time Password) for login.

    This endpoint checks if both the user profile & selected tenant(account) is active.
    """
    # Validate login credentials
    user = await validate_otp_request(db, request.tenant_id, request.username, request.user_identifier_type)

    # Generate User OTP(Expires in 10 minutes)
    otp = await generate_user_otp(db, user)

    # TODO: Need to implement Notification Engine for sending OTP to email or mobile no
    #  based on the "user_identifier_type

    return {
        "message": f"OTP sent successfully: {otp}",
    }


# Step 2-B-2: Verify OTP
@router.post("/otp/verify", response_model=LoginResponse, status_code=status.HTTP_200_OK)
async def verify_otp(request: Annotated[OTPVerifyRequest, Form()],db: AsyncSession = Depends(get_db)):
    """
    Endpoint to verify the OTP (One Time Password) for the user to log in.

    This endpoint checks if both the user profile & selected tenant(account) is active.
    """
    # TODO LoginResponse schema

    # Validate login credentials
    user = await validate_otp_request(db, request.tenant_id, request.username, request.user_identifier_type)

    # Validate User OTP
    await validate_user_otp(user, request.otp)

    default_workspace_id = await get_default_workspace_id(request.tenant_id)

    return {
        "data": {"tenant_id": "", "user_id": "", "user_name": "", "user_image": "", "default_workspace_id": ""},
        "message": "OTP verified, login successful"
    }


# Step 2-B-2: Resend OTP
@router.post("/otp/resend", response_model=Response, status_code=status.HTTP_200_OK)
async def resend_otp(request: Annotated[OTPLoginRequest, Form()],db: AsyncSession = Depends(get_db)):
    """
    Endpoint to resend an OTP (One Time Password) to the user.

    This endpoint checks if both the user profile & selected tenant(account) is active.
    """
    # Validate login credentials
    user = await validate_otp_request(db, request.tenant_id, request.username, request.user_identifier_type)

    # Get or Generate User OTP(Expires in 10 minutes)
    otp = await get_or_generate_user_otp(db, user)

    # TODO: Need to implement Notification Engine for sending OTP to email or mobile no
    #  based on the "user_identifier_type

    return {
        "message": f"OTP resent successfully: {otp}"
    }