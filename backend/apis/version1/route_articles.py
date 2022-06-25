from typing import List
from typing import Optional

from apis.version1.route_login import get_current_user_from_token
from db.models.users import User
from db.repository.articles import create_new_article
from db.repository.articles import delete_article_by_id
from db.repository.articles import list_articles
from db.repository.articles import retrieve_article
from db.repository.articles import search_article
from db.repository.articles import update_article_by_id
from db.session import get_db
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.templating import Jinja2Templates
from schemas.articles import ArticleCreate
from schemas.articles import ShowArticle
from sqlalchemy.orm import Session


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.post("/create-article/",response_model=ShowArticle)
def create_article(
    article: ArticleCreate,
    db: Session = Depends(get_db),
    current_user:User = Depends(get_current_user_from_token),
):
    article = create_new_article(article=article,db=db,owner_id=current_user.id)
    return article


@router.get("/get/{id}",response_model=ShowArticle)
def read_article(id:int,db:Session = Depends(get_db)):
    article = retrieve_article(id=id,db=db)
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Article with this id {id} does not exist")
    return article

@router.get("/all",response_model=List[ShowArticle])
def read_articles(db:Session = Depends(get_db)):
    articles = list_articles(db=db)
    return articles

@router.put("/update/{id}")
def update_article(id: int,article: ArticleCreate,db: Session = Depends(get_db)):
    current_user = 1
    message = update_article_by_id(id=id,article=article,db=db,owner_id=current_user)
    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Article with id {id} not found")
    return {"msg":"Successfully updated data."}

@router.delete("/delete/{id}")
def delete_article(id: int,db: Session = Depends(get_db),current_user: User = Depends(get_current_user_from_token)):
    article = retrieve_article(id=id, db=db)
    if not article:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Article with {id} does not exist")
    print(article.owner_id, current_user.id, current_user.is_superuser)
    if article.owner_id == current_user.id or current_user.is_superuser:
        delete_article_by_id(id=id, db=db, owner_id=current_user.id)
        return {"msg": "Successfully deleted."}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"You are not permitted!!!!")