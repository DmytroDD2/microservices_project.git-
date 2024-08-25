from pydantic import BaseModel


class PostCreate(BaseModel):
    title: str
    content: str
    user_id: int


class Post(PostCreate):
    id: int

    class Config:
        from_attributes = True

