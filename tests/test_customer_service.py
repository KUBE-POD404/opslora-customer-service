import pytest

from app.exceptions.custom_exceptions import ConflictException, NotFoundException
from app.services.customer_service import (
    create_customer_service,
    customer_exists,
    get_customer,
    list_customers_service,
    update_customer,
)


def test_customer_email_is_unique_per_organization(db_session):
    first = create_customer_service(db_session, "Acme", "buyer@example.com", 1, 101)
    second = create_customer_service(db_session, "Acme Other Org", "buyer@example.com", 2, 202)

    assert first.email == second.email
    assert first.organization_id == 1
    assert second.organization_id == 2


def test_customer_duplicate_email_in_same_organization_is_rejected(db_session):
    create_customer_service(db_session, "Acme", "buyer@example.com", 1, 101)

    with pytest.raises(ConflictException):
        create_customer_service(db_session, "Duplicate", "buyer@example.com", 1, 101)


def test_customer_reads_are_tenant_scoped(db_session):
    customer = create_customer_service(db_session, "Acme", "buyer@example.com", 1, 101)

    assert get_customer(db_session, customer.id, 1).id == customer.id
    assert customer_exists(db_session, customer.id, 1)
    assert not customer_exists(db_session, customer.id, 2)
    with pytest.raises(NotFoundException):
        get_customer(db_session, customer.id, 2)


def test_customer_update_prevents_same_org_email_collision(db_session):
    create_customer_service(db_session, "First", "first@example.com", 1, 101)
    second = create_customer_service(db_session, "Second", "second@example.com", 1, 101)

    with pytest.raises(ConflictException):
        update_customer(db_session, second.id, 1, "Second", "first@example.com")


def test_list_customers_returns_only_current_organization(db_session):
    first = create_customer_service(db_session, "First", "first@example.com", 1, 101)
    create_customer_service(db_session, "Other Org", "other@example.com", 2, 202)

    results = list_customers_service(db_session, organization_id=1)

    assert [customer.id for customer in results] == [first.id]
