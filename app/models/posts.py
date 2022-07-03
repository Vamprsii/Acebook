import sqlalchemy

from .users import users_table

metadata = sqlalchemy.MetaData()

posts_table = sqlalchemy.Table(
    "posts",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("users_ids", sqlalchemy.ARRAY(sqlalchemy.Integer)),
    sqlalchemy.Column("status", sqlalchemy.String()),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime()),
    sqlalchemy.Column("title", sqlalchemy.String(100)),
    sqlalchemy.Column("content", sqlalchemy.Text()),
    sqlalchemy.Column("likes", sqlalchemy.Integer()),
    sqlalchemy.Column("liked_by", sqlalchemy.ARRAY(sqlalchemy.Integer)),
    sqlalchemy.Column("views", sqlalchemy.Integer()),
    sqlalchemy.Column("disapprove_comment", sqlalchemy.String()),
    sqlalchemy.Column("section", sqlalchemy.String()),
    sqlalchemy.Column("tags", sqlalchemy.ARRAY(sqlalchemy.String)),
)
