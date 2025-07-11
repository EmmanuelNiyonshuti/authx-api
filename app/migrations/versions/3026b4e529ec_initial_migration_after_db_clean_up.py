"""initial migration after db clean up

Revision ID: 3026b4e529ec
Revises:
Create Date: 2025-07-10 18:25:42.973365

"""

from typing import Sequence, Union



# revision identifiers, used by Alembic.
revision: str = "3026b4e529ec"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
