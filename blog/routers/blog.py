from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
from sqlalchemy.orm import Session
from .. import schemas, database, models,oauth2
from ..repository import blog

router=APIRouter(
    prefix='/blog',
    tags=['Blogs']
    )

get_db =database.get_db
get_current_user=oauth2.get_current_user

@router.get('/',response_model=List[schemas.ShowBlog])
async def all(db: Session = Depends(get_db),current_user: schemas.User=Depends(get_current_user)):
    return blog.get_all(db)

@router.get('/{id}',status_code=200,response_model=schemas.ShowBlog)
async def show(id:int,db: Session = Depends(get_db),current_user: schemas.User=Depends(get_current_user)):
    return blog.show(id, db)

@router.post("",status_code=status.HTTP_201_CREATED)
async def create(request: schemas.Blog,db: Session = Depends(get_db),current_user: schemas.User=Depends(get_current_user)):
    return blog.create(request,db,current_user)

@router.put('/{id}',status_code=status.HTTP_202_ACCEPTED)
async def update(id, request: schemas.Blog,db: Session = Depends(get_db),current_user: schemas.User=Depends(get_current_user)):
    return blog.update(id,request,db)


@router.delete('/{id}',status_code=204)
async def destroy(id: int, db: Session = Depends(get_db),current_user: schemas.User=Depends(get_current_user)):
    return blog.destroy(id,db)

