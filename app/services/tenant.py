import re
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.tenant import Tenant, TenantStatusEnum
from app.utils.helpers import generate_random_string


async def create_tenant(
        db: AsyncSession,
        is_verified: bool,
        company_name: str,
        currency: str = "",
        date_format: str = "",
        time_format: str = "",
        time_zone: str = "",
) -> Tenant:
    """
    Creates a new tenant with the provided details.
    If is_verified, create domain using company name & set the tenant status as active.
    """
    domain = ""
    status = TenantStatusEnum.NOT_VERIFIED

    if is_verified:
        domain = await get_tenant_domain(db, company_name)
        status = TenantStatusEnum.ACTIVE

    # Create the tenant object with all provided details
    tenant = Tenant(
        company_name=company_name,
        domain=domain,
        currency=currency,
        date_format=date_format,
        time_format=time_format,
        time_zone=time_zone,
        status=status
    )

    db.add(tenant)
    await db.commit()
    await db.refresh(tenant)

    return tenant


async def update_tenant(
        db: AsyncSession,
        tenant: Tenant,
        workspace_name: str) -> Tenant:
    """
    Updates the tenant by generating a unique domain using the workspace name.
    Set the tenant status to active.
    """
    currency = ""
    date_format = ""
    time_format = ""
    time_zone = ""
    domain = await get_tenant_domain(db, workspace_name)
    status = TenantStatusEnum.ACTIVE

    # Update tenant details
    tenant.domain = domain
    tenant.currency = currency
    tenant.date_format = date_format
    tenant.time_format = time_format
    tenant.time_zone = time_zone
    tenant.status = status

    await db.commit()
    await db.refresh(tenant)

    return tenant


async def get_tenant_domain(db: AsyncSession, workspace_name: str) -> str:
    """
    Generates a unique domain for the tenant based on the workspace name. If the domain
    already exists, it appends a random string to ensure uniqueness.
    """
    # Sanitize the tenant name to create a domain-friendly format
    formatted_workspace_name = workspace_name.lower()
    formatted_workspace_name = formatted_workspace_name.replace(" ", "-")

    # Remove any non-alphanumeric characters (except hyphens)
    domain = re.sub(r'[^a-z0-9-]', '', formatted_workspace_name)

    # Check if the generated domain already exists in the database
    result = await db.execute(select(Tenant).filter(Tenant.domain == domain))
    existing_domain = result.scalars().first()

    # If the domain already exists, append a random string to make it unique
    while existing_domain:
        domain = f"{domain}{generate_random_string(4)}"
        result = await db.execute(select(Tenant).filter(Tenant.domain == domain))
        existing_domain = result.scalars().first()

    return domain
