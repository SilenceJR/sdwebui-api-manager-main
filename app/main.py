import json
import multiprocessing
import os
from os import path

import uvicorn
from fastapi import FastAPI, HTTPException, Depends, Request, Response
from starlette.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.db import models, curd, schemas
from app.db.database import engine, SessionLocal
from app.db.models import Img2imgArgs, Txt2imgArgs, ExtraSingleImage, ResponseModel
from app.api import api
from app.manager import reqq

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "*",
]

# 将配置挂在到app上
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


# Dependency
def get_db(request: Request):
    return request.state.db


@app.get("/")
def root():
    return {"message": "Fast API in Python"}


@app.post("/rawimg2img", status_code=200)
def rawimg2img(payload: Img2imgArgs):
    payload = payload.dict()

    return api.img2img(payload)


@app.post("/rawtxt2img", status_code=200)
def rawtxt2img(payload: Txt2imgArgs):
    payload = payload.dict()

    return api.txt2img(payload)


@app.post("/img2img", status_code=200)
def img2img(payload: Img2imgArgs):
    payload = payload.dict()
    return reqq.add_req_queue(payload, "img2img")


# @app.post("/txt2img", status_code=200)
# def txt2img(payload: Txt2imgArgs):
#     payload = payload.dict()
#     data = Txt2imgArgs.parse_file("config/sd_config.json")
#     data.prompt = payload.get("prompt") + data.prompt
#     data = data.dict()
#     return reqq.add_req_queue(data, "txt2img")

def txt2img(user: models.User, db: Session):
    data = Txt2imgArgs.parse_file("config/sd_config.json")
    data.prompt = user.prompt + data.prompt
    data = data.dict()
    return reqq.add_req_queue(data, "txt2img", db=db, user=user)


@app.post("/createPortrait", status_code=200)
def create_portrait(user: schemas.UserCreate, db: Session = Depends(get_db)):
    print('111')
    u = curd.create_user(db, user=user)
    return txt2img(u, db=db)


@app.get("/data", status_code=200)
def get_problem():
    data = ResponseModel()
    p = os.path.join(os.getcwd(), 'config', 'data.json')
    print(f'path: {p}')
    try:
        with open(p, "r") as f:
            data.code = 200
            data.data = json.loads(f.read())
    except Exception as e:
        print(e)
        data.code = 201
        data.msg = "數據獲取異常"
    return data


@app.get("/progress/{req_id}")
def progress(req_id: str, db: Session = Depends(get_db)):
    global result
    try:
        result = reqq.get_result(req_id)
        if result['status'] == 'done' or result['status'] == 'finishing':
            image = result['result'].data['images'][0]
            print('1')
            curd.create_user_image(db, models.Image(image=image, description=str(json.dumps(result['payload'])),
                                                    req_id=req_id))
            print('2')

    except Exception as e:
        print(f'err: {e}')
    return result


@app.post("/history")
def history(params: dict, db: Session = Depends(get_db)):

    skip = 0
    if params['skip'] is not None:
        skip = params['skip']

    data = ResponseModel()

    try:
        images = curd.get_images(db=db, skip=skip)
        data.data = images
        data.code = 200

    except Exception as e:
        print(f'err: {e}')
        data.code = 201
    return data


@app.get("/controlnet/model_list")
def controlnet_model_list():
    return api.controlnet_model_list()


@app.get("/controlnet/module_list")
def controlnet_module_list():
    return api.controlnet_module_list()


@app.post("/sdapi/v1/extra-single-image", status_code=200)
def extra_single_image(payload: ExtraSingleImage):
    payload = payload.dict()
    return api.extra_single_image(payload)


@app.get("/sdapi/v1/sd-models")
def sd_models():
    return api.sd_models()


if __name__ == '__main__':
    # multiprocessing.freeze_support()
    # log_config = {
    #     "version": 1,
    #     "disable_existing_loggers": True,
    #     "handlers": {
    #         "file_handler": {
    #             "class": "logging.FileHandler",
    #             "filename": "logfile.log",
    #         },
    #     },
    #     "root": {
    #         "handlers": ["file_handler"],
    #         "level": "INFO",
    #     },
    # }
    # uvicorn.run("app.main:app", host="0.0.0.0", port=5000, reload=True, log_config=log_config)
    uvicorn.run("app.main:app", host="0.0.0.0", port=5000, reload=True)
