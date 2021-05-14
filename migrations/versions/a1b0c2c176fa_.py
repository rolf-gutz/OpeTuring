"""empty message

Revision ID: a1b0c2c176fa
Revises: 166599b7c21b
Create Date: 2021-05-13 23:37:55.025865

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1b0c2c176fa'
down_revision = '166599b7c21b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('itens_pedido',
    sa.Column('id_itens', sa.Integer(), nullable=False),
    sa.Column('id_pedido', sa.Integer(), nullable=False),
    sa.Column('id_produto', sa.Integer(), nullable=False),
    sa.Column('valor', sa.Float(), nullable=True),
    sa.Column('kg', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['id_pedido'], ['pedido.id_pedido'], ),
    sa.ForeignKeyConstraint(['id_produto'], ['produto.idProduto'], ),
    sa.PrimaryKeyConstraint('id_itens')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('itens_pedido')
    # ### end Alembic commands ###
