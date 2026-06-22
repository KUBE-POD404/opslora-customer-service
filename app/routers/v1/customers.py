import logging
from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import (
    CustomerCreate,
    CustomerOrderSnapshot,
    CustomerPortalAccessUpdate,
    CustomerResponse,
    CustomerStatus,
    CustomerStatusUpdate,
    CustomerType,
    CustomerUpdate,
)
from app.services.customer_service import (
    create_customer_service,
    customer_exists,
    get_customer,
    get_customer_order_snapshot,
    list_customers_service,
    update_customer_portal_access,
    update_customer_status,
    update_customer,
)
from app.dependencies.auth import get_current_user
from app.dependencies.permissions import require_permission

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/customers", tags=["Customers"])

DbSession = Annotated[Session, Depends(get_db)]
CurrentCreateUser = Annotated[object, Depends(require_permission("customer.create"))]
CurrentReadUser = Annotated[object, Depends(require_permission("customer.read"))]
CurrentUpdateUser = Annotated[object, Depends(require_permission("customer.update"))]
AuthenticatedUser = Annotated[object, Depends(get_current_user)]


@router.post(
    "/create-customer",
    response_model=CustomerResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_customer_api(
    data: CustomerCreate,
    db: DbSession,
    current_user: CurrentCreateUser,
):
    logger.info("Create customer request received", extra={"email": data.email})
    return create_customer_service(
        db=db,
        payload=data,
        organization_id=current_user.org_id,
        created_by_user_id=current_user.user_id,
    )


@router.get("/", response_model=list[CustomerResponse])
def list_customers(
    db: DbSession,
    current_user: CurrentReadUser,
    page: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=1, le=100)] = 15,
    search: str | None = None,
    status: CustomerStatus | None = None,
    customer_type: CustomerType | None = None,
    portal_access_enabled: bool | None = None,
):
    logger.info("List customers request", extra={"page": page, "limit": limit})
    offset = (page - 1) * limit

    return list_customers_service(
        db,
        organization_id=current_user.org_id,
        offset=offset,
        limit=limit,
        search=search,
        status=status.value if status else None,
        customer_type=customer_type.value if customer_type else None,
        portal_access_enabled=portal_access_enabled,
    )


@router.get("/{customer_id}/exists")
def customer_exists_api(
    customer_id: int,
    db: DbSession,
    current_user: AuthenticatedUser,
):
    logger.info("Check customer exists", extra={"customer_id": customer_id})
    return {
        "exists": customer_exists(
            db,
            customer_id,
            current_user.org_id,
        )
    }


@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer_api(
    customer_id: int,
    db: DbSession,
    current_user: CurrentReadUser,
):
    logger.info("Get customer", extra={"customer_id": customer_id})
    return get_customer(
        db,
        customer_id,
        current_user.org_id,
    )


@router.get("/{customer_id}/order-snapshot", response_model=CustomerOrderSnapshot)
def get_customer_order_snapshot_api(
    customer_id: int,
    db: DbSession,
    current_user: CurrentReadUser,
):
    logger.info("Get customer order snapshot", extra={"customer_id": customer_id})
    return get_customer_order_snapshot(
        db,
        customer_id,
        current_user.org_id,
    )


@router.put("/{customer_id}", response_model=CustomerResponse)
def update_customer_api(
    customer_id: int,
    payload: CustomerUpdate,
    db: DbSession,
    current_user: CurrentUpdateUser,
):
    logger.info("Update customer", extra={"customer_id": customer_id})
    return update_customer(
        db=db,
        customer_id=customer_id,
        organization_id=current_user.org_id,
        payload=payload,
    )


@router.patch("/{customer_id}/status", response_model=CustomerResponse)
def update_customer_status_api(
    customer_id: int,
    payload: CustomerStatusUpdate,
    db: DbSession,
    current_user: CurrentUpdateUser,
):
    logger.info("Update customer status", extra={"customer_id": customer_id})
    return update_customer_status(
        db=db,
        customer_id=customer_id,
        organization_id=current_user.org_id,
        status=payload.status,
    )


@router.patch("/{customer_id}/portal-access", response_model=CustomerResponse)
def update_customer_portal_access_api(
    customer_id: int,
    payload: CustomerPortalAccessUpdate,
    db: DbSession,
    current_user: CurrentUpdateUser,
):
    logger.info("Update customer portal access", extra={"customer_id": customer_id})
    return update_customer_portal_access(
        db=db,
        customer_id=customer_id,
        organization_id=current_user.org_id,
        portal_access_enabled=payload.portal_access_enabled,
    )
