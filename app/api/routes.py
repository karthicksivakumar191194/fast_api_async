from fastapi import APIRouter

from app.api.controllers.heartbeat import router as heartbeat_router
from app.api.controllers.onboarding.v1.onboarding import router as onboarding_router
from app.api.controllers.login.v1.sass_app import router as saas_app_login_router
from app.api.controllers.login.v1.tenant_portal import router as tenant_portal_login_router


api_router = APIRouter()

# Include all routes
api_router.include_router(heartbeat_router, prefix="/v1/heartbeat", tags=["Heartbeat"])
api_router.include_router(onboarding_router, prefix="/v1/onboard", tags=["Onboard Tenant"])
api_router.include_router(saas_app_login_router, prefix="/v1/saas-app/login", tags=["Login via SaaS Application"])
api_router.include_router(tenant_portal_login_router, prefix="/v1/tenant-portal/login", tags=["Login via Tenant Portal"])
