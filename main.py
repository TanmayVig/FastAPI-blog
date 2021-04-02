import uvicorn
from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()

@app.get('/blog')
async def index(limit: int, published: bool=True, sort:Optional[str]=None):
    # only get 10 published blogs
    if published: # works for http://127.0.0.1:8000/blog?limit=20&published=true
        return {'data':f'{limit} blogs from blog list'}

@app.get('/blog/unpublished')
async def unpublished():
    return {'data':'all unpublished blogs'}

@app.get('/blog/{id}')
async def show(id: int):
    return {'data': id}


@app.get('/blog/{id}/comments')
async def commets(id,limit:int=10):
    return {'data':['1','2','3'],'limit':limit}

class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]


@app.post('/blog')
async def create_blog(blog: Blog):
    return {'data': f'blog is created with title {blog.title}'}


# if __name__ == "__main__":
#     uvicorn.run(app,host="127.0.0.1",port=9000)