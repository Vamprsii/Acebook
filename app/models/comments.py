
import sqlalchemy

from .users import users_table
from .posts import posts_table

metadata = sqlalchemy.MetaData()

comments_table = sqlalchemy.Table(
    "comments",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("post_id", sqlalchemy.ForeignKey(posts_table.c.id)),
    sqlalchemy.Column("user_id", sqlalchemy.ForeignKey(users_table.c.id)),
    sqlalchemy.Column("comment", sqlalchemy.Text()),
)
