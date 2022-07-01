from datetime import datetime

from app.models.database import database
from app.models.drafts import drafts_table
from app.schemas import drafts as draft_schema
from sqlalchemy import desc, func, select


async def create_draft(draft: draft_schema.DraftModel, user):
    query = (
        drafts_table.insert()
        .values(
            title=draft.title,
            content=draft.content,
            users_ids=[user["id"]],
            status="draft",
        )
        .returning(
            drafts_table.c.id,
            drafts_table.c.title,
            drafts_table.c.content,
            drafts_table.c.users_ids,
            drafts_table.c.status,
        )
    )
    draft = await database.fetch_one(query)

    # Convert to dict and add user_name key to it
    draft = dict(zip(draft, draft.values()))
    return draft


async def get_draft(draft_id: int):
    query = (
        select(
            [
                drafts_table.c.id,
                drafts_table.c.title,
                drafts_table.c.content,
                drafts_table.c.users_ids,
                drafts_table.c.status,
            ]
        )
        .select_from(drafts_table)
        .where(drafts_table.c.id == draft_id)
    )
    return await database.fetch_one(query)


async def get_drafts(page: int):
    max_per_page = 10
    offset1 = (page - 1) * max_per_page
    query = (
        select(
            [
                drafts_table.c.id,
                drafts_table.c.title,
                drafts_table.c.content,
                drafts_table.c.users_ids,
                drafts_table.c.status,
            ]
        )
        .select_from(drafts_table)
        .order_by(desc(drafts_table.c.id))
        .limit(max_per_page)
        .offset(offset1)
    )
    return await database.fetch_all(query)


async def get_drafts_count():
    query = select([func.count()]).select_from(drafts_table)
    return await database.fetch_val(query)


async def delete_draft_by_id(draft_id):
    query = f'DELETE FROM drafts WHERE id={draft_id};'
    await database.execute(query)


async def update_draft(draft_id: int, draft: draft_schema.DraftModel):
    query = (
        drafts_table.update()
        .where(drafts_table.c.id == draft_id)
        .values(title=draft.title, content=draft.content)
    )
    return await database.execute(query)
