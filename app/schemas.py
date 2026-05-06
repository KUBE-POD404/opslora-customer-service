from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class CustomerType(str, Enum):
    BUSINESS = "BUSINESS"
    INDIVIDUAL = "INDIVIDUAL"


class CustomerStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class CustomerBase(BaseModel):
    name: str
    email: EmailStr
    display_name: str | None = Field(default=None, max_length=150)
    phone: str | None = Field(default=None, max_length=50)
    customer_type: CustomerType = CustomerType.BUSINESS
    status: CustomerStatus = CustomerStatus.ACTIVE
    contact_person_name: str | None = Field(default=None, max_length=150)
    contact_person_email: EmailStr | None = None
    contact_person_phone: str | None = Field(default=None, max_length=50)
    tax_id: str | None = Field(default=None, max_length=50)
    gstin: str | None = Field(default=None, max_length=20)
    tax_registration_type: str | None = Field(default=None, max_length=50)
    place_of_supply: str | None = Field(default=None, max_length=100)
    billing_address_line1: str | None = Field(default=None, max_length=255)
    billing_address_line2: str | None = Field(default=None, max_length=255)
    billing_city: str | None = Field(default=None, max_length=100)
    billing_state: str | None = Field(default=None, max_length=100)
    billing_postal_code: str | None = Field(default=None, max_length=30)
    billing_country: str | None = Field(default=None, max_length=100)
    shipping_same_as_billing: bool = True
    shipping_address_line1: str | None = Field(default=None, max_length=255)
    shipping_address_line2: str | None = Field(default=None, max_length=255)
    shipping_city: str | None = Field(default=None, max_length=100)
    shipping_state: str | None = Field(default=None, max_length=100)
    shipping_postal_code: str | None = Field(default=None, max_length=30)
    shipping_country: str | None = Field(default=None, max_length=100)
    payment_terms_days: int | None = Field(default=None, ge=0, le=365)
    notes: str | None = None
    portal_access_enabled: bool = False

    @field_validator(
        "display_name",
        "phone",
        "contact_person_name",
        "contact_person_email",
        "contact_person_phone",
        "tax_id",
        "gstin",
        "tax_registration_type",
        "place_of_supply",
        "billing_address_line1",
        "billing_address_line2",
        "billing_city",
        "billing_state",
        "billing_postal_code",
        "billing_country",
        "shipping_address_line1",
        "shipping_address_line2",
        "shipping_city",
        "shipping_state",
        "shipping_postal_code",
        "shipping_country",
        "notes",
        mode="before",
    )
    @classmethod
    def empty_string_to_none(cls, value):
        if isinstance(value, str) and not value.strip():
            return None
        return value


class CustomerCreate(CustomerBase):
    name: str = Field(..., min_length=2, max_length=100)


class CustomerResponse(CustomerBase):
    id: int
    email: EmailStr
    created_at: datetime
    updated_at: datetime | None = None
    portal_invited_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class CustomerUpdate(CustomerBase):
    name: str = Field(..., min_length=2, max_length=100)
