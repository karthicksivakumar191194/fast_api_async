from fastapi import APIRouter, status


router = APIRouter()

# User enters email or mobile number & password
@router.post("/", status_code=status.HTTP_200_OK)
async def login(request):
    """
    Endpoint to validate the email address or mobile number and password for the provided tenant(account).

    This endpoint checks if both the user profile & tenant(account) is active.
    """
    tenant_id = ""

    # TODO Functionality

    # Sample Response
    return {
        "data": {"tenant_id": "", "user_id": "", "user_name": "", "user_image": "", "default_workspace_id": ""},
        "message": "Logged in successfully"
    }


#  User requests OTP for login
@router.post("/otp", status_code=status.HTTP_200_OK)
async def request_otp(request):
    """
    Endpoint to request an OTP (One Time Password) for login.

    This endpoint checks if both the user profile & tenant(account) is active.
    """
    tenant_id = ""

    # TODO Functionality

    return {
        "message": "OTP sent successfully"
    }


# Verify OTP
@router.post("/otp/verify", status_code=status.HTTP_200_OK)
async def verify_otp(request):
    """
    Endpoint to verify the OTP (One Time Password) for the user to log in.

    This endpoint checks if both the user profile & tenant(account) is active.
    """
    tenant_id = ""

    # TODO Functionality

    return {
        "data": {"tenant_id": "", "user_id": "", "user_name": "", "user_image": "", "default_workspace_id": ""},
        "message": "OTP verified, login successful"
    }

# Resend OTP
@router.post("/otp/resend", status_code=status.HTTP_200_OK)
async def resend_otp(request):
    """
    Endpoint to resend an OTP (One Time Password) to the user.

    This endpoint checks if both the user profile & tenant(account) is active.
    """
    tenant_id = ""

    # TODO Functionality

    return {
        "message": "OTP resent successfully"
    }