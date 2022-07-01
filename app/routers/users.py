from app.schemas import users
from app.utils import users as users_utils
from app.utils.dependencies import get_current_user
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.utils.role_checker import RoleChecker

router = APIRouter()

admin_only = RoleChecker(["admin"])
moderator_only = RoleChecker(["moderator", "admin"])


@router.get("/", dependencies=[Depends(get_current_user)])
async def health_check():
    return {"Hello": "World"}


# ВСЕ ХОРОШО
@router.post("/auth", response_model=users.TokenBase)
async def auth(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await users_utils.get_user_by_email(email=form_data.username)

    if not user:
        raise HTTPException(
            status_code=400, detail="Incorrect email or password")
    if not users_utils.validate_password(
        password=form_data.password, hashed_password=user["hashed_password"]
    ):
        raise HTTPException(
            status_code=400, detail="Incorrect email or password")

    return await users_utils.create_user_token(user_id=user["id"])


# ВСЕ ХОРОШО
@router.post("/sign-up", response_model=users.User)
async def create_user(user: users.UserCreate):
    db_user = await users_utils.get_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await users_utils.create_user(user=user)


# ВСЕ ХОРОШО
@router.post("/users/block", response_model=users.User, dependencies=[Depends(get_current_user), Depends(admin_only)])
async def block_user(email: str):
    db_user = await users_utils.get_user_by_email(email=email)
    if not db_user:
        raise HTTPException(
            status_code=400, detail="User with this email not found")
    await users_utils.block_user(email=email)
    return await users_utils.get_user_by_email(email=email)


# ВСЕ ХОРОШО
@router.post("/users/unblock", response_model=users.User, dependencies=[Depends(get_current_user), Depends(admin_only)])
async def unblock_user(email: str):
    db_user = await users_utils.get_user_by_email(email=email)
    if not db_user:
        raise HTTPException(
            status_code=400, detail="User with this email not found")
    await users_utils.unblock_user(email=email)
    return await users_utils.get_user_by_email(email=email)

# ВСЕ ХОРОШО


@router.post("/users/add_role", response_model=users.User, dependencies=[Depends(get_current_user), Depends(admin_only)])
async def add_user_role(email: str, role: str):
    if role not in ["admin", "moderator", "editor", "user"]:
        raise HTTPException(
            status_code=400, detail="Entered role not in available roles list")
    db_user = await users_utils.get_user_by_email(email=email)
    if db_user is None:
        raise HTTPException(
            status_code=400, detail="User with this email not found")
    roles: list = db_user["roles"]
    print(roles)
    if role not in roles:
        roles += [role]
    else:
        raise HTTPException(
            status_code=400, detail="User already have this role")
    await users_utils.change_user_role(email=email, roles=roles)
    return await users_utils.get_user_by_email(email=email)


@router.post("/users/remove_role", response_model=users.User, dependencies=[Depends(get_current_user), Depends(admin_only)])
async def add_user_role(email: str, role: str):
    if role not in ["admin", "moderator", "editor", "user"]:
        raise HTTPException(
            status_code=400, detail="Entered role not in available roles list")
    db_user = await users_utils.get_user_by_email(email=email)
    if db_user is None:
        raise HTTPException(
            status_code=400, detail="User with this email not found")
    roles: list = db_user["roles"]
    print(roles)
    if role not in roles:
        raise HTTPException(
            status_code=400, detail="User does not have this role")
    else:
        roles.remove(role)
    await users_utils.change_user_role(email=email, roles=roles)
    return await users_utils.get_user_by_email(email=email)

# ВСЕ ХОРОШО


@router.get("/users/me", response_model=users.UserBase)
async def read_users_me(current_user: users.User = Depends(get_current_user)):
    return current_user


# ВСЕ ХОРОШО
@router.get("/users/all", response_model=list, dependencies=[Depends(get_current_user), Depends(admin_only)])
async def get_all_users(users: list = Depends(users_utils.get_all_users)):
    return users
