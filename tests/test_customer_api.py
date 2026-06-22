from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.dependencies.auth import get_current_user
from app.main import app
from app.models.customer import Customer  # noqa: F401
from app.security.jwt import TokenPayload


def test_customer_api_crud_and_exists_contract():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    def override_current_user():
        return TokenPayload(
            user_id=10,
            org_id=20,
            permissions=["customer.create", "customer.read", "customer.update"],
        )

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_current_user

    try:
        client = TestClient(app)

        create_response = client.post(
            "/api/v1/customers/create-customer",
            json={
                "name": "Acme Buyer",
                "display_name": "Acme",
                "email": "buyer@example.com",
                "phone": "+91-9876543210",
                "customer_type": "BUSINESS",
                "gstin": "29ABCDE1234F1Z5",
                "place_of_supply": "Karnataka",
                "billing_city": "Bengaluru",
                "billing_country": "India",
                "portal_access_enabled": True,
            },
        )

        assert create_response.status_code == 201
        created = create_response.json()
        assert created["name"] == "Acme Buyer"
        assert created["email"] == "buyer@example.com"
        assert created["display_name"] == "Acme"
        assert created["gstin"] == "29ABCDE1234F1Z5"
        assert created["portal_access_enabled"] is True

        customer_id = created["id"]

        list_response = client.get("/api/v1/customers/")
        assert list_response.status_code == 200
        assert [customer["id"] for customer in list_response.json()] == [customer_id]

        filtered_response = client.get("/api/v1/customers/?search=ABCDE&portal_access_enabled=true")
        assert filtered_response.status_code == 200
        assert [customer["id"] for customer in filtered_response.json()] == [customer_id]

        exists_response = client.get(f"/api/v1/customers/{customer_id}/exists")
        assert exists_response.status_code == 200
        assert exists_response.json() == {"exists": True}

        snapshot_response = client.get(f"/api/v1/customers/{customer_id}/order-snapshot")
        assert snapshot_response.status_code == 200
        assert snapshot_response.json()["gstin"] == "29ABCDE1234F1Z5"

        portal_response = client.patch(
            f"/api/v1/customers/{customer_id}/portal-access",
            json={"portal_access_enabled": False},
        )
        assert portal_response.status_code == 200
        assert portal_response.json()["portal_access_enabled"] is False

        update_response = client.put(
            f"/api/v1/customers/{customer_id}",
            json={
                "name": "Acme Updated",
                "email": "updated@example.com",
                "phone": "+91-9999999999",
                "customer_type": "BUSINESS",
                "status": "ACTIVE",
                "shipping_same_as_billing": False,
                "shipping_city": "Mysuru",
                "shipping_country": "India",
                "portal_access_enabled": False,
            },
        )
        assert update_response.status_code == 200
        assert update_response.json()["name"] == "Acme Updated"
        assert update_response.json()["email"] == "updated@example.com"
        assert update_response.json()["phone"] == "+91-9999999999"
        assert update_response.json()["shipping_same_as_billing"] is False
        assert update_response.json()["portal_access_enabled"] is False

        status_response = client.patch(
            f"/api/v1/customers/{customer_id}/status",
            json={"status": "INACTIVE"},
        )
        assert status_response.status_code == 200
        assert status_response.json()["status"] == "INACTIVE"

        inactive_snapshot_response = client.get(f"/api/v1/customers/{customer_id}/order-snapshot")
        assert inactive_snapshot_response.status_code == 409
    finally:
        app.dependency_overrides.clear()
        Base.metadata.drop_all(bind=engine)
