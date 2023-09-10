from pydantic import BaseModel


class ImageBase(BaseModel):
    description: str
    req_id: str


class ImageCreate(ImageBase):
    image: str


class Image(ImageBase):
    id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    name: str
    prompt: str


class UserCreate(UserBase):
    reply: str


class User(UserCreate):
    id: int
    req_id: str

    class Config:
        orm_mode = True
