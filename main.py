from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

# Fast-App
app = FastAPI()


# Model

class BlogModel(BaseModel):
    title: str
    body: str
    published: Optional[bool]


@app.post('/blog')
def create_blog(request: BlogModel):
    return {
        "message": "Blog is created",
        "data": f'{request}',
    }


@app.get('/blog')  # ?limit=10&published=true
def blog(limit: int = 10, published: bool = False, sort: Optional[str] = None):
    if published:
        return {"blogs": f"{limit} published blog list."}
    else:
        return {"blogs": f"{limit} blog list."}


@app.get('/user/{name}')
def index(name: str):
    return {"status": "Welcome " + name + ", FastAPI's world"}

# Debugging and Change Port
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=9000)
