from typing import List

from fastapi import Depends, HTTPException

from app.schemas.users import User
from app.utils.dependencies import get_current_user


class RoleChecker:
    def __init__(self, allowed_roles: List):
        self.allowed_roles = allowed_roles

    def __call__(self, user: User = Depends(get_current_user)):
        print(user["roles"], self.allowed_roles)
        flag = False
        for role in user["roles"]:
            if role in self.allowed_roles:
                flag = True
        if not flag:
            raise HTTPException(
                status_code=403, detail="Operation not permitted")
