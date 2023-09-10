from sqlalchemy.orm import Session

from app.db import models, schemas
from app.db.database import SessionLocal


# from . import models, schemas


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(name=user.name, reply=user.reply, prompt=user.prompt)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user: models.User):
    i = db.query(models.User).where(models.User.id == user.id).update({"req_id": user.req_id}, )
    db.commit()
    return i
    # db.commit()
    # return id


def get_images(db: Session, skip: int = 0, limit: int = 20):
    return db.query(models.Image).offset(skip).limit(limit).all()


def get_image(db: Session, req_id: str):
    return db.query(models.Image).filter(models.Image.req_id == req_id).first()


def get_user_image(db: Session, req_id: str, skip: int = 0, limit: int = 100):
    return db.query(models.Image).filter(schemas.Image.req_id == req_id).offset(skip).limit(limit).all()


def create_user_image(db: Session, image: schemas.ImageCreate):
    db_image = models.Image(req_id=image.req_id, description=image.description, image=image.image)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image

# if __name__ == '__main__':
#     image = create_user_image(SessionLocal, user_id=0, sd_id="123", i="456", description='789')
#     print(f"image: {image}")
# import sqlite3
#
# conn = sqlite3.connect("../../config/db.db")
#
