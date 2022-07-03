from datetime import datetime
import typing

from app.models.database import database
from app.models.posts import posts_table
from app.schemas import posts as post_schema
from sqlalchemy import desc, func, select


async def create_post(post: post_schema.PostModel, user):
    query = (
        posts_table.insert()
        .values(
            title=post.title,
            content=post.content,
            created_at=datetime.now(),
            users_ids=[user["id"]],
            status="published",
            likes=0,
            views=0,
            liked_by=[],
            section="",
            tags=[],
        )
        .returning(
            posts_table.c.id,
            posts_table.c.title,
            posts_table.c.content,
            posts_table.c.created_at,
            posts_table.c.users_ids,
            posts_table.c.status,
            posts_table.c.likes,
            posts_table.c.views,
            posts_table.c.liked_by,
            posts_table.c.section,
            posts_table.c.tags,
        )
    )
    post = await database.fetch_one(query)

    # Convert to dict and add user_name key to it
    post = dict(zip(post, post.values()))
    return post


async def get_post(post_id: int):
    query = (
        select(
            [
                posts_table.c.id,
                posts_table.c.title,
                posts_table.c.content,
                posts_table.c.created_at,
                posts_table.c.users_ids,
                posts_table.c.status,
                posts_table.c.likes,
                posts_table.c.views,
                posts_table.c.disapprove_comment,
                posts_table.c.liked_by,
                posts_table.c.section,
                posts_table.c.tags,
            ]
        )
        .select_from(posts_table)
        .where(posts_table.c.id == post_id)
    )
    return await database.fetch_one(query)


async def delete_post_by_id(post_id):
    query = f'DELETE FROM posts WHERE id={post_id};'
    await database.execute(query)


async def increase_views_post_on_get(post_id: int, views: int):
    query = posts_table.update().values(
        views=views).where(posts_table.c.id == post_id)
    await database.execute(query)


async def like_post(post_id: int, liked_by: list, likes: int):
    query = posts_table.update().values(
        likes=likes, liked_by=liked_by).where(posts_table.c.id == post_id)
    await database.execute(query)


async def post_section(post_id: int, section: str):
    query = posts_table.update().values(
        section=section).where(posts_table.c.id == post_id)
    await database.execute(query)


async def post_tags(post_id: int, tags: list):
    query = posts_table.update().values(
        tags=tags).where(posts_table.c.id == post_id)
    await database.execute(query)


async def get_posts(page: int):
    max_per_page = 10
    offset1 = (page - 1) * max_per_page
    query = (
        select(
            [
                posts_table.c.id,
                posts_table.c.created_at,
                posts_table.c.title,
                posts_table.c.content,
                posts_table.c.users_ids,
                posts_table.c.likes,
                posts_table.c.views,
                posts_table.c.status,
                posts_table.c.liked_by,
                posts_table.c.section,
                posts_table.c.tags,
            ]
        )
        .select_from(posts_table)
        .order_by(desc(posts_table.c.created_at))
        .limit(max_per_page)
        .offset(offset1)
    )
    return await database.fetch_all(query)


async def get_posts_approved_only(page: int):
    max_per_page = 10
    offset1 = (page - 1) * max_per_page
    query = (
        select(
            [
                posts_table.c.id,
                posts_table.c.created_at,
                posts_table.c.title,
                posts_table.c.content,
                posts_table.c.users_ids,
                posts_table.c.likes,
                posts_table.c.views,
                posts_table.c.status,
                posts_table.c.liked_by,
                posts_table.c.section,
                posts_table.c.tags,
            ]
        )
        .select_from(posts_table)
        .where(posts_table.c.status == "approved")
        .order_by(desc(posts_table.c.created_at))
        .limit(max_per_page)
        .offset(offset1)
    )
    return await database.fetch_all(query)


async def get_posts_approved_only_likes_order(page: int):
    max_per_page = 10
    offset1 = (page - 1) * max_per_page
    query = (
        select(
            [
                posts_table.c.id,
                posts_table.c.created_at,
                posts_table.c.title,
                posts_table.c.content,
                posts_table.c.users_ids,
                posts_table.c.likes,
                posts_table.c.views,
                posts_table.c.status,
                posts_table.c.liked_by,
                posts_table.c.section,
                posts_table.c.tags,
            ]
        )
        .select_from(posts_table)
        .where(posts_table.c.status == "approved")
        .order_by(posts_table.c.likes.desc())
        .limit(max_per_page)
        .offset(offset1)
    )
    return await database.fetch_all(query)


async def get_posts_approved_only_views_order(page: int):
    max_per_page = 10
    offset1 = (page - 1) * max_per_page
    query = (
        select(
            [
                posts_table.c.id,
                posts_table.c.created_at,
                posts_table.c.title,
                posts_table.c.content,
                posts_table.c.users_ids,
                posts_table.c.likes,
                posts_table.c.views,
                posts_table.c.status,
                posts_table.c.liked_by,
                posts_table.c.section,
                posts_table.c.tags,
            ]
        )
        .select_from(posts_table)
        .where(posts_table.c.status == "approved")
        .order_by(desc(posts_table.c.views))
        .limit(max_per_page)
        .offset(offset1)
    )
    return await database.fetch_all(query)


async def get_posts_approved_only_title(page: int, search_string: str):
    max_per_page = 10
    offset1 = (page - 1) * max_per_page
    query = (
        select(
            [
                posts_table.c.id,
                posts_table.c.created_at,
                posts_table.c.title,
                posts_table.c.content,
                posts_table.c.users_ids,
                posts_table.c.likes,
                posts_table.c.views,
                posts_table.c.status,
                posts_table.c.liked_by,
                posts_table.c.section,
                posts_table.c.tags,
            ]
        )
        .select_from(posts_table)
        .where(posts_table.c.status == "approved")
        .order_by(desc(posts_table.c.created_at))
        .limit(max_per_page)
        .offset(offset1)
    )
    posts = await database.fetch_all(query)
    _posts = [post for post in posts if (search_string in post["title"])]
    return _posts


async def get_posts_approved_only_content(page: int, search_string: str):
    max_per_page = 10
    offset1 = (page - 1) * max_per_page
    query = (
        select(
            [
                posts_table.c.id,
                posts_table.c.created_at,
                posts_table.c.title,
                posts_table.c.content,
                posts_table.c.users_ids,
                posts_table.c.likes,
                posts_table.c.views,
                posts_table.c.status,
                posts_table.c.liked_by,
                posts_table.c.section,
                posts_table.c.tags,
            ]
        )
        .select_from(posts_table)
        .where(posts_table.c.status == "approved")
        .order_by(desc(posts_table.c.created_at))
        .limit(max_per_page)
        .offset(offset1)
    )
    posts = await database.fetch_all(query)
    _posts = [post for post in posts if (search_string in post["content"])]
    return _posts


async def get_posts_approved_only_authors(page: int, search_string: str):
    max_per_page = 10
    offset1 = (page - 1) * max_per_page
    query = (
        select(
            [
                posts_table.c.id,
                posts_table.c.created_at,
                posts_table.c.title,
                posts_table.c.content,
                posts_table.c.users_ids,
                posts_table.c.likes,
                posts_table.c.views,
                posts_table.c.status,
                posts_table.c.liked_by,
                posts_table.c.section,
                posts_table.c.tags,
            ]
        )
        .select_from(posts_table)
        .where(posts_table.c.status == "approved")
        .order_by(desc(posts_table.c.created_at))
        .limit(max_per_page)
        .offset(offset1)
    )
    posts = await database.fetch_all(query)
    _posts = [post for post in posts if (
        int(search_string) in post["users_ids"])]
    return _posts


async def get_posts_approved_only_tags(page: int, search_string: str):
    max_per_page = 10
    offset1 = (page - 1) * max_per_page
    query = (
        select(
            [
                posts_table.c.id,
                posts_table.c.created_at,
                posts_table.c.title,
                posts_table.c.content,
                posts_table.c.users_ids,
                posts_table.c.likes,
                posts_table.c.views,
                posts_table.c.status,
                posts_table.c.liked_by,
                posts_table.c.section,
                posts_table.c.tags,
            ]
        )
        .select_from(posts_table)
        .where(posts_table.c.status == "approved")
        .order_by(desc(posts_table.c.created_at))
        .limit(max_per_page)
        .offset(offset1)
    )
    posts = await database.fetch_all(query)
    _posts = [post for post in posts if (search_string in post["tags"])]
    return _posts


async def get_posts_published_only(page: int):
    max_per_page = 10
    offset1 = (page - 1) * max_per_page
    query = (
        select(
            [
                posts_table.c.id,
                posts_table.c.created_at,
                posts_table.c.title,
                posts_table.c.content,
                posts_table.c.users_ids,
                posts_table.c.likes,
                posts_table.c.views,
                posts_table.c.status,
                posts_table.c.liked_by,
                posts_table.c.section,
                posts_table.c.tags,
            ]
        )
        .select_from(posts_table)
        .where(posts_table.c.status == "published")
        .order_by(desc(posts_table.c.created_at))
        .limit(max_per_page)
        .offset(offset1)
    )
    return await database.fetch_all(query)


async def get_posts_count():
    query = select([func.count()]).select_from(posts_table)
    return await database.fetch_val(query)


async def get_posts_count_approved_only():
    query = select([func.count()]).select_from(
        posts_table).where(posts_table.c.status == "approved")
    return await database.fetch_val(query)


async def get_posts_count_published_only():
    query = select([func.count()]).select_from(
        posts_table).where(posts_table.c.status == "published")
    return await database.fetch_val(query)


async def update_post(post_id: int, post: post_schema.PostModel):
    query = (
        posts_table.update()
        .where(posts_table.c.id == post_id)
        .values(title=post.title, content=post.content, status="published", disapprove_comment=None)
    )
    return await database.execute(query)


async def update_post_status(post_id: int, status: str, disapprove_comment: typing.Optional[str] = ""):
    # ПО ХОРОШЕМУ ТУТ ДОЛЖНА БЫТЬ ПРОВЕРКА НА ТО ЧТО СТАТУС ЕСТЬ В СПИСКЕ ВОЗМОЖНЫХ, НО МНЕ ПУФИК!!! ☆*: .｡. o(≧▽≦)o .｡.:*☆
    if status == "disapproved":
        query = (
            posts_table.update()
            .where(posts_table.c.id == post_id)
            .values(status=status, disapprove_comment=disapprove_comment)
        )
    else:
        query = (
            posts_table.update()
            .where(posts_table.c.id == post_id)
            .values(status=status)
        )
    return await database.execute(query)
