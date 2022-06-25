from datetime import date
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


# shared properties
class ArticleBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    text: Optional[str] = None
    date_posted: Optional[date] = datetime.now().date()


# this will be used to validate data while creating an Article
class ArticleCreate(ArticleBase):
    title: str
    description: str
    text: str


# this will be used to format the response to not to have id,owner_id etc
class ShowArticle(ArticleBase):
    title: str
    date_posted: date
    description: Optional[str]
    text: str

    class Config():  # to convert non dict obj to json
        orm_mode = True