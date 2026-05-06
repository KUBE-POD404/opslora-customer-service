import logging
from datetime import datetime, timezone
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.exceptions.custom_exceptions import NotFoundException, ConflictException
from app.schemas import CustomerCreate, CustomerStatus, CustomerUpdate

logger = logging.getLogger(__name__)


def create_customer_service(
    db: Session,
    payload: CustomerCreate,
    organization_id: int,
    created_by_user_id: int
) -> Customer:

    logger.info("Creating customer", extra={"email": payload.email})

    existing = (
        db.query(Customer)
        .filter(
            Customer.organization_id == organization_id,
            Customer.email == payload.email,
        )
        .first()
    )
    if existing:
        raise ConflictException("Customer email already exists in this organization")

    customer = Customer(
        organization_id=organization_id,
        **payload.model_dump(),
        created_by_user_id=created_by_user_id,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    db.add(customer)

    try:
        db.commit()
        db.refresh(customer)
        logger.info("Customer created", extra={"customer_id": customer.id})
        return customer
    except IntegrityError:
        db.rollback()
        logger.warning("Customer email conflict", extra={"email": payload.email})
        raise ConflictException("Customer email already exists in this organization")


def get_customer(db: Session, customer_id: int, organization_id: int) -> Customer:

    logger.info("Fetching customer", extra={"customer_id": customer_id})

    customer = (
        db.query(Customer)
        .filter(
            Customer.id == customer_id,
            Customer.organization_id == organization_id
        )
        .first()
    )

    if not customer:
        logger.warning("Customer not found", extra={"customer_id": customer_id})
        raise NotFoundException("Customer not found")

    return customer


def list_customers_service(
    db: Session,
    organization_id: int,
    offset: int = 0,
    limit: int = 15,
    search: str | None = None,
    status: str | None = None,
    customer_type: str | None = None,
    portal_access_enabled: bool | None = None,
):
    logger.info("Listing customers", extra={"offset": offset, "limit": limit})

    query = db.query(Customer).filter(Customer.organization_id == organization_id)

    if search:
        pattern = f"%{search.strip()}%"
        query = query.filter(
            Customer.name.ilike(pattern)
            | Customer.display_name.ilike(pattern)
            | Customer.email.ilike(pattern)
            | Customer.phone.ilike(pattern)
            | Customer.gstin.ilike(pattern)
        )

    if status:
        query = query.filter(Customer.status == status)

    if customer_type:
        query = query.filter(Customer.customer_type == customer_type)

    if portal_access_enabled is not None:
        query = query.filter(Customer.portal_access_enabled == portal_access_enabled)

    return query.order_by(Customer.id.desc()).offset(offset).limit(limit).all()


def update_customer(
    db: Session,
    customer_id: int,
    organization_id: int,
    payload: CustomerUpdate,
):
    logger.info("Updating customer", extra={"customer_id": customer_id})

    customer = get_customer(db, customer_id, organization_id)

    existing = (
        db.query(Customer)
        .filter(
            Customer.organization_id == organization_id,
            Customer.email == payload.email,
            Customer.id != customer_id,
        )
        .first()
    )
    if existing:
        raise ConflictException("Customer email already exists in this organization")

    for field, value in payload.model_dump().items():
        setattr(customer, field, value)
    customer.updated_at = datetime.now(timezone.utc)

    try:
        db.commit()
        db.refresh(customer)
        logger.info("Customer updated", extra={"customer_id": customer.id})
        return customer
    except IntegrityError:
        db.rollback()
        logger.warning("Email conflict on update", extra={"email": payload.email})
        raise ConflictException("Email already exists")


def customer_exists(
    db: Session,
    customer_id: int,
    organization_id: int
) -> bool:

    logger.info("Checking customer existence", extra={"customer_id": customer_id})

    customer = (
        db.query(Customer)
        .filter(
            Customer.id == customer_id,
            Customer.organization_id == organization_id
        )
        .first()
    )

    return customer is not None


def update_customer_status(
    db: Session,
    customer_id: int,
    organization_id: int,
    status: CustomerStatus,
) -> Customer:
    customer = get_customer(db, customer_id, organization_id)
    customer.status = status.value if hasattr(status, "value") else status
    customer.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(customer)
    return customer


def update_customer_portal_access(
    db: Session,
    customer_id: int,
    organization_id: int,
    portal_access_enabled: bool,
) -> Customer:
    customer = get_customer(db, customer_id, organization_id)
    customer.portal_access_enabled = portal_access_enabled
    customer.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(customer)
    return customer


def get_customer_order_snapshot(
    db: Session,
    customer_id: int,
    organization_id: int,
) -> Customer:
    customer = get_customer(db, customer_id, organization_id)
    if customer.status != CustomerStatus.ACTIVE.value:
        raise ConflictException("Customer is inactive")
    return customer
