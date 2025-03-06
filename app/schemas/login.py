from pydantic import BaseModel, Field
from typing import List

from app.models import UserIdentifierType
from app.schemas.base_schema import Request


class UserTenant(BaseModel):
    tenant_id: str
    tenant_domain: str
    company_name: str
    company_logo: str
    user_id: str
    user_name: str
    user_image: str


class UserTenantListResponse(BaseModel):
    data: List[UserTenant]


class LoginRequestBaseSchema(Request):
    tenant_id: str
    username: str
    user_identifier_type: UserIdentifierType


class LoginRequest(LoginRequestBaseSchema):
    password: str = Field(..., min_length=8)


class OTPLoginRequest(LoginRequestBaseSchema):
    pass

class OTPVerifyRequest(LoginRequestBaseSchema):
    otp: str = Field(..., min_length=6)

class LoginResponse(BaseModel):
    data: str
