from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from .. import models, schemas

def get_all(db: Session):
    blogs=db.query(models.Blog).all()
    return blogs

def create(request: schemas.Blog,db: Session,current_user):
    user=db.query(models.User).filter(models.User.email==current_user.email).first()
    new_blog = models.Blog(title=request.title, body=request.body,user_id=user.id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def destroy(id:int,db: Session):
    blog_delete=db.query(models.Blog).filter(models.Blog.id == id)
    if not blog_delete.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail="blog not found")
    blog_delete.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

def update(id: int, request: schemas.Blog, db: Session):
    blog_update=db.query(models.Blog).filter(models.Blog.id == id)
    if not blog_update.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail="blog not found")
        
    blog_update.update(dict(request), synchronize_session=False)
    db.commit()
    return "updated"

def show(id: int, db: Session):
    one_blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not one_blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Blog with id {id} does not exist.')
    return one_blog