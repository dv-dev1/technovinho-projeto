"""enforce availability constraints

Revision ID: 002
Revises: 001
Create Date: 2026-05-25

"""

from typing import Sequence, Union

from alembic import op

revision: str = "002"
down_revision: Union[str, None] = "001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_check_constraint(
        "ck_availability_day_of_week",
        "availability",
        "day_of_week BETWEEN 0 AND 6",
    )
    op.create_check_constraint(
        "ck_availability_time_range",
        "availability",
        "end_time > start_time",
    )


def downgrade() -> None:
    op.drop_constraint("ck_availability_time_range", "availability", type_="check")
    op.drop_constraint("ck_availability_day_of_week", "availability", type_="check")
