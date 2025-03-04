from fastapi import APIRouter, status


router = APIRouter()

# Step 1: User enters email or mobile number
@router.post("/", status_code=status.HTTP_200_OK)
async def login_with_email_or_mobile(request):
    """
    Endpoint to retrieve active user accounts based on email address or mobile number.

    This endpoint checks the status of user profile associated with the provided
    email address or mobile number. For each active user profile found, it checks if
    the associated tenant is active. If the tenant is active, it returns the
    tenant's details along with the associated user account information.
    """
    # TODO Functionality

    # Sample Response
    return {
        "data": [
            {"tenant_id": "", "company_name": "", "company_logo": "", "user_id": "", "user_name": "", "user_image": ""}
        ],
        "message": "Success"
    }


# Step 2-A: User enters password
@router.post("/password", status_code=status.HTTP_200_OK)
async def login_with_password(request):
    """
    Endpoint to validate the email address or mobile number and password for the selected tenant(account).

    This endpoint checks if both the user profile & selected tenant(account) is active.
    """

    # TODO Functionality

    return {
        "data": {"tenant_id": "", "user_id": "", "user_name": "", "user_image": "", "default_workspace_id": ""},
        "message": "Logged in successfully"
    }


# Step 2-B-1: User requests OTP for login
@router.post("/otp", status_code=status.HTTP_200_OK)
async def request_otp(request):
    """
    Endpoint to request an OTP (One Time Password) for login.

    This endpoint checks if both the user profile & selected tenant(account) is active.
    """
    # TODO Functionality

    return {
        "message": "OTP sent successfully"
    }


# Step 2-B-2: Verify OTP
@router.post("/otp/verify", status_code=status.HTTP_200_OK)
async def verify_otp(request):
    """
    Endpoint to verify the OTP (One Time Password) for the user to log in.

    This endpoint checks if both the user profile & selected tenant(account) is active.
    """
    # TODO Functionality

    return {
        "data": {"tenant_id": "", "user_id": "", "user_name": "", "user_image": "", "default_workspace_id": ""},
        "message": "OTP verified, login successful"
    }

# Step 2-B-2: Resend OTP
@router.post("/otp/resend", status_code=status.HTTP_200_OK)
async def resend_otp(request):
    """
    Endpoint to resend an OTP (One Time Password) to the user.

    This endpoint checks if both the user profile & selected tenant(account) is active.
    """
    # TODO Functionality

    return {
        "message": "OTP resent successfully"
    }