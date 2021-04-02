from typing import List
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas
from . import schemas, models
from .database import engine,SessionLocal

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/blog",status_code=status.HTTP_201_CREATED)
async def create(request: schemas.Blog,db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get('/blogs',response_model=List[schemas.ShowBlog])
async def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.put('/blog/{id}',status_code=status.HTTP_202_ACCEPTED)
async def update(id, request: schemas.Blog,db: Session = Depends(get_db)):
    blog_update=db.query(models.Blog).filter(models.Blog.id == id)
    if not blog_update.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail="blog not found")
        
    blog_update.update(dict(request), synchronize_session=False)
    db.commit()
    return "updated"

@app.delete('/blog/{id}',status_code=204)
async def destroy(id: int, db: Session = Depends(get_db)):
    blog_delete=db.query(models.Blog).filter(models.Blog.id == id)
    if not blog_delete.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail="blog not found")
    blog_delete.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get('/blog/{id}',status_code=200,response_model=schemas.ShowBlog)
async def show(id:int, response: Response,db: Session = Depends(get_db)):
    one_blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not one_blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Blog with id {id} does not exist.')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail':f'Blog with id {id} does not exist.'}
    return one_blog
    

@app.post('/user')
async def create_user(request: schemas.User,db: Session = Depends(get_db)):
    new_user=models.User(name=request.name, email=request.email, password=request.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

