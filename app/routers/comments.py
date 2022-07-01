from app.schemas.users import User
from app.utils import comments as comments_utils
from app.utils import posts as post_utils
from app.utils.dependencies import get_current_user
from fastapi import APIRouter, Depends, HTTPException, status
from app.utils.role_checker import RoleChecker

router = APIRouter()

admin_only = RoleChecker(["admin"])
moderator_only = RoleChecker(["moderator", "admin"])
editor_only = RoleChecker(["editor", "admin"])


@router.get("/comments/{post_id}", status_code=201, dependencies=[Depends(get_current_user)])
async def get_comments(post_id: int):
    post = await post_utils.get_post(post_id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Post with this ID is not found",
        )
    return await comments_utils.get_comments_for_post(post_id=post_id)


@router.post("/comments/{post_id}", status_code=201)
async def create_comment(post_id: int, comment: str, current_user: User = Depends(get_current_user)):
    post = await post_utils.get_post(post_id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Post with this ID is not found",
        )
    await comments_utils.add_comment(post_id=post_id, user_id=current_user["id"], comment=comment)
    return await comments_utils.get_comments_for_post(post_id=post_id)


@router.post("/comments/delete/{post_id}", status_code=201)
async def delete_comment(post_id: int, comment_id: int, current_user: User = Depends(get_current_user)):
    '''Проверка пренадлежит коментарий человеку или нет не нужна так как и так передается пользователь'''
    post = await post_utils.get_post(post_id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Post with this ID is not found",
        )
    await comments_utils.delete_comment(post_id=post_id, user_id=current_user["id"], comment_id=comment_id)
    return await comments_utils.get_comments_for_post(post_id=post_id)


@router.post("/comments/delete/moderator/{post_id}", status_code=201, dependencies=[Depends(moderator_only)])
async def moderator_delete_comment(post_id: int, comment_id: int):
    post = await post_utils.get_post(post_id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Post with this ID is not found",
        )
    await comments_utils.delete_comment_by_id(post_id=post_id, comment_id=comment_id)
    return await comments_utils.get_comments_for_post(post_id=post_id)
