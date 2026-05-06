from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text, UniqueConstraint
from datetime import datetime, timezone
from app.database import Base

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    display_name = Column(String(150), nullable=True)
    email = Column(String(150), nullable=False)
    phone = Column(String(50), nullable=True)
    customer_type = Column(String(30), nullable=False, default="BUSINESS")
    status = Column(String(30), nullable=False, default="ACTIVE")
    contact_person_name = Column(String(150), nullable=True)
    contact_person_email = Column(String(150), nullable=True)
    contact_person_phone = Column(String(50), nullable=True)
    tax_id = Column(String(50), nullable=True)
    gstin = Column(String(20), nullable=True)
    tax_registration_type = Column(String(50), nullable=True)
    place_of_supply = Column(String(100), nullable=True)
    billing_address_line1 = Column(String(255), nullable=True)
    billing_address_line2 = Column(String(255), nullable=True)
    billing_city = Column(String(100), nullable=True)
    billing_state = Column(String(100), nullable=True)
    billing_postal_code = Column(String(30), nullable=True)
    billing_country = Column(String(100), nullable=True)
    shipping_same_as_billing = Column(Boolean, nullable=False, default=True)
    shipping_address_line1 = Column(String(255), nullable=True)
    shipping_address_line2 = Column(String(255), nullable=True)
    shipping_city = Column(String(100), nullable=True)
    shipping_state = Column(String(100), nullable=True)
    shipping_postal_code = Column(String(30), nullable=True)
    shipping_country = Column(String(100), nullable=True)
    payment_terms_days = Column(Integer, nullable=True)
    notes = Column(Text, nullable=True)
    portal_access_enabled = Column(Boolean, nullable=False, default=False)
    portal_invited_at = Column(DateTime(timezone=True), nullable=True)
    created_by_user_id = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))

    __table_args__ = (
        UniqueConstraint("organization_id", "email", name="uq_customers_org_email"),
    )
