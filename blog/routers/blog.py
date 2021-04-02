from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from sqlalchemy.orm import Session
from .. import schemas, database, models
from ..repository import blog

router=APIRouter(
    prefix='/blog',
    tags=['Blogs']
    )

get_db =database.get_db

@router.get('/',response_model=List[schemas.ShowBlog])
async def all(db: Session = Depends(get_db)):
    return blog.get_all(db)

@router.get('/{id}',status_code=200,response_model=schemas.ShowBlog)
async def show(id:int,db: Session = Depends(get_db)):
    return blog.show(id, db)

@router.post("",status_code=status.HTTP_201_CREATED)
async def create(request: schemas.Blog,db: Session = Depends(get_db)):
    return blog.create(request,db)

@router.put('/{id}',status_code=status.HTTP_202_ACCEPTED)
async def update(id, request: schemas.Blog,db: Session = Depends(get_db)):
    return blog.update(id,request,db)


@router.delete('/{id}',status_code=204)
async def destroy(id: int, db: Session = Depends(get_db)):
    return blog.destroy(id,db)

