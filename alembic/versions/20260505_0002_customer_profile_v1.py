"""customer profile v1

Revision ID: 20260505_0002
Revises: 20260501_0001
Create Date: 2026-05-05
"""

from alembic import op
import sqlalchemy as sa

revision = "20260505_0002"
down_revision = "20260501_0001"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("customers", sa.Column("display_name", sa.String(length=150), nullable=True))
    op.add_column("customers", sa.Column("phone", sa.String(length=50), nullable=True))
    op.add_column(
        "customers",
        sa.Column("customer_type", sa.String(length=30), nullable=False, server_default="BUSINESS"),
    )
    op.add_column(
        "customers",
        sa.Column("status", sa.String(length=30), nullable=False, server_default="ACTIVE"),
    )
    op.add_column("customers", sa.Column("contact_person_name", sa.String(length=150), nullable=True))
    op.add_column("customers", sa.Column("contact_person_email", sa.String(length=150), nullable=True))
    op.add_column("customers", sa.Column("contact_person_phone", sa.String(length=50), nullable=True))
    op.add_column("customers", sa.Column("tax_id", sa.String(length=50), nullable=True))
    op.add_column("customers", sa.Column("gstin", sa.String(length=20), nullable=True))
    op.add_column("customers", sa.Column("tax_registration_type", sa.String(length=50), nullable=True))
    op.add_column("customers", sa.Column("place_of_supply", sa.String(length=100), nullable=True))
    op.add_column("customers", sa.Column("billing_address_line1", sa.String(length=255), nullable=True))
    op.add_column("customers", sa.Column("billing_address_line2", sa.String(length=255), nullable=True))
    op.add_column("customers", sa.Column("billing_city", sa.String(length=100), nullable=True))
    op.add_column("customers", sa.Column("billing_state", sa.String(length=100), nullable=True))
    op.add_column("customers", sa.Column("billing_postal_code", sa.String(length=30), nullable=True))
    op.add_column("customers", sa.Column("billing_country", sa.String(length=100), nullable=True))
    op.add_column(
        "customers",
        sa.Column("shipping_same_as_billing", sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.add_column("customers", sa.Column("shipping_address_line1", sa.String(length=255), nullable=True))
    op.add_column("customers", sa.Column("shipping_address_line2", sa.String(length=255), nullable=True))
    op.add_column("customers", sa.Column("shipping_city", sa.String(length=100), nullable=True))
    op.add_column("customers", sa.Column("shipping_state", sa.String(length=100), nullable=True))
    op.add_column("customers", sa.Column("shipping_postal_code", sa.String(length=30), nullable=True))
    op.add_column("customers", sa.Column("shipping_country", sa.String(length=100), nullable=True))
    op.add_column("customers", sa.Column("payment_terms_days", sa.Integer(), nullable=True))
    op.add_column("customers", sa.Column("notes", sa.Text(), nullable=True))
    op.add_column(
        "customers",
        sa.Column("portal_access_enabled", sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    op.add_column("customers", sa.Column("portal_invited_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column(
        "customers",
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )


def downgrade():
    op.drop_column("customers", "updated_at")
    op.drop_column("customers", "portal_invited_at")
    op.drop_column("customers", "portal_access_enabled")
    op.drop_column("customers", "notes")
    op.drop_column("customers", "payment_terms_days")
    op.drop_column("customers", "shipping_country")
    op.drop_column("customers", "shipping_postal_code")
    op.drop_column("customers", "shipping_state")
    op.drop_column("customers", "shipping_city")
    op.drop_column("customers", "shipping_address_line2")
    op.drop_column("customers", "shipping_address_line1")
    op.drop_column("customers", "shipping_same_as_billing")
    op.drop_column("customers", "billing_country")
    op.drop_column("customers", "billing_postal_code")
    op.drop_column("customers", "billing_state")
    op.drop_column("customers", "billing_city")
    op.drop_column("customers", "billing_address_line2")
    op.drop_column("customers", "billing_address_line1")
    op.drop_column("customers", "place_of_supply")
    op.drop_column("customers", "tax_registration_type")
    op.drop_column("customers", "gstin")
    op.drop_column("customers", "tax_id")
    op.drop_column("customers", "contact_person_phone")
    op.drop_column("customers", "contact_person_email")
    op.drop_column("customers", "contact_person_name")
    op.drop_column("customers", "status")
    op.drop_column("customers", "customer_type")
    op.drop_column("customers", "phone")
    op.drop_column("customers", "display_name")
