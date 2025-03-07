from pydantic import BaseModel, Field, EmailStr
from typing import Optional

from app.schemas.base_schema import Request, CreateResponse


class OnboardRequest(Request):
    company_name: Optional[str] = None
    owner_name: str = Field(..., min_length=1)
    owner_email: EmailStr
    owner_password: str = Field(..., min_length=8)
