import pytest

from app.exceptions.custom_exceptions import ConflictException, NotFoundException
from app.schemas import CustomerCreate, CustomerUpdate
from app.services.customer_service import (
    create_customer_service,
    customer_exists,
    get_customer,
    list_customers_service,
    update_customer,
)


def customer_payload(name="Acme", email="buyer@example.com", **overrides):
    data = {
        "name": name,
        "email": email,
    }
    data.update(overrides)
    return CustomerCreate(**data)


def test_customer_email_is_unique_per_organization(db_session):
    first = create_customer_service(db_session, customer_payload(), 1, 101)
    second = create_customer_service(
        db_session,
        customer_payload(name="Acme Other Org"),
        2,
        202,
    )

    assert first.email == second.email
    assert first.organization_id == 1
    assert second.organization_id == 2


def test_customer_duplicate_email_in_same_organization_is_rejected(db_session):
    create_customer_service(db_session, customer_payload(), 1, 101)

    with pytest.raises(ConflictException):
        create_customer_service(db_session, customer_payload(name="Duplicate"), 1, 101)


def test_customer_reads_are_tenant_scoped(db_session):
    customer = create_customer_service(db_session, customer_payload(), 1, 101)

    assert get_customer(db_session, customer.id, 1).id == customer.id
    assert customer_exists(db_session, customer.id, 1)
    assert not customer_exists(db_session, customer.id, 2)
    with pytest.raises(NotFoundException):
        get_customer(db_session, customer.id, 2)


def test_customer_update_prevents_same_org_email_collision(db_session):
    create_customer_service(db_session, customer_payload("First", "first@example.com"), 1, 101)
    second = create_customer_service(db_session, customer_payload("Second", "second@example.com"), 1, 101)

    with pytest.raises(ConflictException):
        update_customer(
            db_session,
            second.id,
            1,
            CustomerUpdate(name="Second", email="first@example.com"),
        )


def test_list_customers_returns_only_current_organization(db_session):
    first = create_customer_service(db_session, customer_payload("First", "first@example.com"), 1, 101)
    create_customer_service(db_session, customer_payload("Other Org", "other@example.com"), 2, 202)

    results = list_customers_service(db_session, organization_id=1)

    assert [customer.id for customer in results] == [first.id]


def test_customer_profile_fields_are_persisted(db_session):
    customer = create_customer_service(
        db_session,
        customer_payload(
            name="Acme Pvt Ltd",
            email="accounts@acme.example.com",
            display_name="Acme",
            phone="+91-9876543210",
            gstin="29ABCDE1234F1Z5",
            place_of_supply="Karnataka",
            billing_city="Bengaluru",
            billing_country="India",
            shipping_same_as_billing=True,
            payment_terms_days=30,
            portal_access_enabled=True,
        ),
        1,
        101,
    )

    assert customer.customer_type == "BUSINESS"
    assert customer.status == "ACTIVE"
    assert customer.display_name == "Acme"
    assert customer.gstin == "29ABCDE1234F1Z5"
    assert customer.portal_access_enabled is True
    assert customer.payment_terms_days == 30
