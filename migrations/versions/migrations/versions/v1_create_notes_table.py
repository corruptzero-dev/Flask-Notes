from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'note',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String(64), index=True),
        sa.Column('body', sa.String(120)),
        sa.Column('status', sa.String(20))
    )

def downgrade():
    op.drop_table('note')