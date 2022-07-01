from datetime import datetime

from pydantic import BaseModel


class DraftModel(BaseModel):
    """ Validate request data """
    title: str
    content: str


class DraftDetailsModel(DraftModel):
    """ Return response data """
    id: int
    users_ids: list
    status: str
