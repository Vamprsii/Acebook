import typing
from app.schemas.drafts import DraftModel
from app.schemas.posts import PostDetailsModel, PostModel
from app.schemas.users import User
from app.utils import posts as post_utils
from app.utils.dependencies import get_current_user
from fastapi import APIRouter, Depends, HTTPException, status
from app.utils.drafts import create_draft
from app.utils.role_checker import RoleChecker
from datetime import datetime

router = APIRouter()

admin_only = RoleChecker(["admin"])
moderator_only = RoleChecker(["moderator", "admin"])
editor_only = RoleChecker(["editor", "admin"])


# ВСЕ ХОРОШО
@router.post("/posts", response_model=PostDetailsModel, status_code=201, dependencies=[Depends(editor_only)])
async def create_post(post: PostModel, current_user: User = Depends(get_current_user)):
    post = await post_utils.create_post(post, current_user)
    return post


# ВСЕ ХОРОШО
@router.get("/posts", dependencies=[Depends(get_current_user)])
async def get_posts(page: int = 1, sort_type: typing.Optional[str] = None, search_string: typing.Optional[str] = None):
    '''Выводит только одобренные модератором статьи (status=="approved")'''
    total_count = await post_utils.get_posts_count_approved_only()
    if sort_type is not None:
        if sort_type == "likes":
            posts = await post_utils.get_posts_approved_only_likes_order(page)
        elif sort_type == "views":
            posts = await post_utils.get_posts_approved_only_views_order(page)
        elif sort_type == "title":
            if search_string is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No search string given",
                )
            posts = await post_utils.get_posts_approved_only_title(page, search_string)
        elif sort_type == "content":
            if search_string is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No search string given",
                )
            posts = await post_utils.get_posts_approved_only_content(page, search_string)
        elif sort_type == "tags":
            if search_string is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No search string given",
                )
            posts = await post_utils.get_posts_approved_only_tags(page, search_string)
        elif sort_type == "authors":
            if search_string is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No search string given",
                )
            posts = await post_utils.get_posts_approved_only_authors(page, search_string)
        elif sort_type == "date":
            if search_string is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No search string given",
                )
            posts = await post_utils.get_posts_approved_only(page)
            # ПЕРЕДАТЬ КОЛ-ВО ЧАСОВ СКОЛЬКО ПРОШЛО ОТ ВЫКЛАДКИ ПОСТА
            _posts = [post for post in posts if ((
                abs(post["created_at"] - datetime.now()).total_seconds()) / 3600 < int(search_string))]
            return {"total_count": total_count, "results": _posts}
    else:
        posts = await post_utils.get_posts_approved_only(page)
    return {"total_count": total_count, "results": posts}


@ router.get("/posts/latest", dependencies=[Depends(get_current_user)])
async def get_posts_latest(page: int = 1):
    posts = await post_utils.get_posts_approved_only(page)
    _posts = [post for post in posts if (
        (abs(post["created_at"] - datetime.now()).total_seconds()) / 3600 < 12)]
    return {"total_count": len(_posts), "results": _posts}


# ИЗМЕНИТЬ ПРАВА ДОСТУПА К ТОЧКЕ
@ router.get("/posts/published", dependencies=[Depends(moderator_only), Depends(get_current_user)])
async def get_posts_published(page: int = 1):
    '''Выводит только статьи для модератора (status=="published")'''
    total_count = await post_utils.get_posts_count_published_only()
    posts = await post_utils.get_posts_published_only(page)
    return {"total_count": total_count, "results": posts}


# ВСЕ ХОРОШО
@ router.get("/posts/{post_id}", response_model=PostDetailsModel, dependencies=[Depends(get_current_user)])
async def get_post(post_id: int):
    post = await post_utils.get_post(post_id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Post with this ID not found",
        )
    else:
        await post_utils.increase_views_post_on_get(post["id"], int(post["views"]) + 1)
    return await post_utils.get_post(post_id)


@ router.post("/posts/like/{post_id}", response_model=PostDetailsModel, status_code=201)
async def like_post(post_id: int, current_user: User = Depends(get_current_user)):
    post = await post_utils.get_post(post_id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Post with this ID not found",
        )
    else:
        if current_user["id"] in post["liked_by"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You have already liked this post",
            )
        else:
            liked_by: list = post["liked_by"] + [current_user["id"]]
            await post_utils.like_post(post_id, liked_by, int(post["likes"]) + 1)
            post = await post_utils.get_post(post_id)
            return post


@ router.post("/posts/dislike/{post_id}", response_model=PostDetailsModel, status_code=201)
async def dislike_post(post_id: int, current_user: User = Depends(get_current_user)):
    post = await post_utils.get_post(post_id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Post with this ID not found",
        )
    else:
        if current_user["id"] in post["liked_by"]:
            liked_by: list = post["liked_by"]
            liked_by.remove(current_user["id"])
            await post_utils.like_post(post_id, liked_by, int(post["likes"]) - 1)
            post = await post_utils.get_post(post_id)
            return post

        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You have not rated this post",
            )


# ВСЕ ХОРОШО
@ router.put("/posts/{post_id}", response_model=PostDetailsModel, dependencies=[Depends(editor_only), Depends(get_current_user)])
async def update_post(
    post_id: int, post_data: PostModel, current_user=Depends(get_current_user)
):
    post = await post_utils.get_post(post_id)
    if post["status"] == "approved":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot modify approved post. Move it to draft and edit things you want",
        )
    if current_user["id"] not in post["users_ids"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to modify this post",
        )
    await post_utils.update_post(post_id=post_id, post=post_data)
    return await post_utils.get_post(post_id)


# ВСЕ ХОРОШО
@ router.put("/posts/todraft/{post_id}", dependencies=[Depends(editor_only), Depends(get_current_user)])
async def move_post_to_draft(
    post_id: int, current_user=Depends(get_current_user)
):
    post = await post_utils.get_post(post_id)
    if current_user["id"] not in post["users_ids"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to modify this post",
        )
    draft = await create_draft(DraftModel(title=post["title"], content=post["content"]), current_user)
    await post_utils.delete_post_by_id(post_id)
    return draft


# ПРАВА МОДЕРАТОРА
@ router.put("/posts/approve/{post_id}", response_model=PostDetailsModel, dependencies=[Depends(moderator_only), Depends(get_current_user)])
async def approve_post(post_id: int):
    await post_utils.update_post_status(post_id=post_id, status="approved")
    return await post_utils.get_post(post_id)


# ПРАВА МОДЕРАТОРА
@ router.put("/posts/disapprove/{post_id}", response_model=PostDetailsModel, dependencies=[Depends(moderator_only), Depends(get_current_user)])
async def disapprove_post(post_id: int, disapprove_comment: str):
    await post_utils.update_post_status(post_id=post_id, status="disapproved", disapprove_comment=disapprove_comment)
    post = await post_utils.get_post(post_id)
    if disapprove_comment == "":
        disapprove_comment = "Post was disapproved with no comments given."
    return {**post, "disapprove_comment": disapprove_comment}


@ router.put("/posts/section/{post_id}", response_model=PostDetailsModel, dependencies=[Depends(moderator_only), Depends(get_current_user)], status_code=201)
async def update_post_section(post_id: int, section: str):
    post = await post_utils.get_post(post_id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Post with this ID not found",
        )
    else:
        await post_utils.post_section(post_id, section)
        post = await post_utils.get_post(post_id)
        return post


@ router.put("/posts/tag/{post_id}", response_model=PostDetailsModel, dependencies=[Depends(moderator_only), Depends(get_current_user)], status_code=201)
async def update_post_tags(post_id: int, tag: str):
    post = await post_utils.get_post(post_id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Post with this ID not found",
        )
    else:
        tags: list = post["tags"]
        tags.append(tag)
        await post_utils.post_tags(post_id, tags)
        post = await post_utils.get_post(post_id)
        return post
