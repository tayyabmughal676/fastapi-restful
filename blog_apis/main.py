from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.post('/blog', status_code=status.HTTP_201_CREATED)
async def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return {
        "code": 1,
        "message": "New blog created",
        "data": new_blog,
    }


@app.get('/blog')
async def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return {
        "code": 1,
        "message": "All data loaded",
        "data": blogs,
    }


@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    print(f"blog -> {blog.first()}")
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Data not found for delete")

    blog.delete(synchronize_session = False)
    db.commit()
    return {
        "code": 1,
        "message": "Data deleted",
        "data": "Not found",
    }


@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
async def update(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    print(f"id: {id}")
    print(f"blogRequest -> {request}")
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    print(f"blog -> {blog.first()}")
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Data not found for update")

    blog.update(request, synchronize_session=False)
    db.commit()

    return {
        "code": 1,
        "message": "Data loaded",
        "data": blog,
    }


@app.get('/blog/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
async def show(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Data not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {
        #     "code": 0,
        # "message": f"Data not found with id: {id}.",
        #     "data": []
        #     }
    return {
        "code": 1,
        "message": "Data loaded",
        "data": blog,
    }
