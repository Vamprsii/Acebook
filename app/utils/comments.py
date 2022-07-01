import hashlib
import random
import string
from datetime import datetime, timedelta
import typing
from sqlalchemy import and_

from app.models.database import database
from app.models.users import tokens_table, users_table
from app.models.comments import comments_table
from app.schemas import users as user_schema


async def add_comment(post_id: int, user_id: int, comment: str):
    query = comments_table.insert().values(
        post_id=post_id, user_id=user_id, comment=comment)
    await database.execute(query)


async def delete_comment(post_id: int, user_id: int, comment_id: str):
    query = f'DELETE FROM comments WHERE post_id={post_id} and user_id={user_id} and id={comment_id};'
    await database.execute(query)


async def delete_comment_by_id(post_id: int, comment_id: str):
    query = f'DELETE FROM comments WHERE post_id={post_id} and id={comment_id};'
    await database.execute(query)


async def get_comments_for_post(post_id: int):
    query = comments_table.select().where(comments_table.c.post_id == post_id)
    return await database.fetch_all(query)


async def get_comment_for_post(post_id: int, user_id: int, comment_id: int):
    query = comments_table.select().where(comments_table.c.post_id == post_id,
                                          comments_table.c.user_id == user_id,
                                          comments_table.c.comment_id == comment_id)
    return await database.fetch_one(query)
