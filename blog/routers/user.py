from sys import prefix
from blog import database, schemas
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import database,schemas, models
from ..repository import user

router = APIRouter(
    prefix="/user",
    tags=['Users']
    )

get_db=database.get_db

@router.post('/',response_model=schemas.ShowUser)
async def create_user(request: schemas.User,db: Session = Depends(get_db)):
    return user.create(request,db)

@router.get('/{id}',response_model=schemas.ShowUser)
async def get_user(id: int, db: Session = Depends(get_db)):
    return user.show(id, db)
