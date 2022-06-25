from fastapi import APIRouter
from fastapi import Request,Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from db.repository.articles import list_articles
from db.session import get_db



templates = Jinja2Templates(directory="templates")
router = APIRouter(include_in_schema=False)


@router.get("/")
async def home(request: Request,db: Session = Depends(get_db)):
    articles = list_articles(db=db)
    return templates.TemplateResponse(
        "general_pages/homepage.html", {"request": request,"articles":articles}
    )