from datetime import datetime
import typing

from pydantic import BaseModel


class PostModel(BaseModel):
    """ Validate request data """
    title: str
    content: str


class PostDetailsModel(PostModel):
    """ Return response data """
    id: int
    users_ids: list
    created_at: datetime
    likes: int
    views: int
    status: str
    disapprove_comment: typing.Optional[str]
    liked_by: list
