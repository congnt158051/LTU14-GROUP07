import time
import uuid
import numpy as np
from PIL import Image
from starlette.requests import Request
import io
import base64
import json
import os

import redis
from fastapi import FastAPI, File, HTTPException

app = FastAPI()
db = redis.StrictRedis(host='redis')

@app.get("/")
def hello():
    return "Hello World!"

@app.post("/predict")
def predict(request: Request, img_file: bytes=File(...)):
    data = {"success": False}
    if request.method == "POST":
        image = Image.open(io.BytesIO(img_file))
        if image.mode != "RGB":
            image = image.convert("RGB")
        image = np.array(image)
        height_image = image.shape[0]
        width_image = image.shape[1]
        
        image = image.copy(order="C")

        k = str(uuid.uuid4())
        image = base64.b64encode(image).decode("utf-8")
        d = {"id": k, "image": image, "height":height_image, "width": width_image}
        db.rpush('image_queue', json.dumps(d))