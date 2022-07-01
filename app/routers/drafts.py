from app.schemas.drafts import DraftDetailsModel, DraftModel
from app.schemas.posts import PostModel
from app.schemas.users import User
from app.utils import drafts as draft_utils
from app.utils.dependencies import get_current_user
from fastapi import APIRouter, Depends, HTTPException, status
from app.utils.posts import create_post
from app.utils.role_checker import RoleChecker

router = APIRouter()

admin_only = RoleChecker(["admin"])
moderator_only = RoleChecker(["moderator", "admin"])
editor_only = RoleChecker(["editor", "admin"])


# ВСЕ ХОРОШО
@router.post("/drafts", response_model=DraftDetailsModel, status_code=201, dependencies=[Depends(moderator_only), Depends(get_current_user)])
async def create_draft(draft: DraftModel, current_user: User = Depends(get_current_user)):
    draft = await draft_utils.create_draft(draft, current_user)
    return draft


# ВСЕ ХОРОШО
@router.get("/drafts", dependencies=[Depends(admin_only), Depends(get_current_user)])
async def get_drafts(page: int = 1):
    '''ДЕБАГ ФИЧА ДЛЯ АДМИНА'''
    total_count = await draft_utils.get_drafts_count()
    drafts = await draft_utils.get_drafts(page)
    return {"total_count": total_count, "results": drafts}


# ВСЕ ХОРОШО
@router.get("/drafts/{draft_id}", response_model=DraftDetailsModel, dependencies=[Depends(editor_only)])
async def get_draft(draft_id: int, current_user=Depends(get_current_user)):
    draft = await draft_utils.get_draft(draft_id)
    if current_user["id"] not in draft["users_ids"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to look at this draft",
        )
    return await draft_utils.get_draft(draft_id)


# ВСЕ ХОРОШО
@router.put("/drafts/{draft_id}", response_model=DraftDetailsModel, dependencies=[Depends(editor_only), Depends(get_current_user)])
async def update_draft(
    draft_id: int, draft_data: DraftModel, current_user=Depends(get_current_user)
):
    draft = await draft_utils.get_draft(draft_id)
    if current_user["id"] not in draft["users_ids"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to modify this draft post",
        )
    await draft_utils.update_draft(draft_id=draft_id, draft=draft_data)
    return await draft_utils.get_draft(draft_id)

# ВСЕ ХОРОШО


@router.put("/posts/topost/{draft_id}", dependencies=[Depends(editor_only), Depends(get_current_user)])
async def move_draft_to_post(
    draft_id: int, current_user=Depends(get_current_user)
):
    draft = await draft_utils.get_draft(draft_id)
    if current_user["id"] not in draft["users_ids"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to modify this draft",
        )
    post = await create_post(PostModel(title=draft["title"], content=draft["content"]), current_user)
    await draft_utils.delete_draft_by_id(draft_id)
    return post
