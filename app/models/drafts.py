import sqlalchemy

from .users import users_table

metadata = sqlalchemy.MetaData()

drafts_table = sqlalchemy.Table(
    "drafts",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer(), primary_key=True),
    sqlalchemy.Column("users_ids", sqlalchemy.ARRAY(sqlalchemy.Integer)),
    sqlalchemy.Column("title", sqlalchemy.String(100)),
    sqlalchemy.Column("content", sqlalchemy.Text()),
    sqlalchemy.Column("status", sqlalchemy.String()),
)
