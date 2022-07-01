import uvicorn
from app.models.database import database
from app.routers import posts, users, drafts, comments
from fastapi import FastAPI
from app.utils.users import get_user_by_email, create_user
from app.schemas.users import UserCreate

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()
    if await get_user_by_email("admin@admin.com") == None:
        await create_user(UserCreate(email="admin@admin.com", name="admin", password="admin"), ["admin"])
    if await get_user_by_email("moderator@moderator.com") == None:
        await create_user(UserCreate(email="moderator@moderator.com", name="moderator", password="moderator"), ["moderator"])
    if await get_user_by_email("editor@editor.com") == None:
        await create_user(UserCreate(email="editor@editor.com", name="editor", password="editor"), ["editor"])
    if await get_user_by_email("user@user.com") == None:
        await create_user(UserCreate(email="user@user.com", name="user", password="user"), ["user"])


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(users.router)
app.include_router(posts.router)
app.include_router(drafts.router)
app.include_router(comments.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
