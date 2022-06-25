from typing import List
from typing import Optional

from fastapi import Request


class JobCreateForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.title: Optional[str] = None
        self.description: Optional[str] = None
        self.text: Optional[str] = None

    async def load_data(self):
        form = await self.request.form()
        self.title = form.get("title")
        self.description = form.get("description")
        self.text = form.get("text")

    def is_valid(self):
        if not self.title or not len(self.title) >= 4:
            self.errors.append("A valid title is required")
        if not self.description or not len(self.description) >= 20:
            self.errors.append("Description too short")
        if not self.text or not len(self.text) >= 20:
            self.errors.append("Article is too short")
        if not self.errors:
            return True
        return False
