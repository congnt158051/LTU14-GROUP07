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
db = redis.StrictRedis(host=os.environ.get("REDIS_HOST"))

CLIENT_MAX_TRIES = int(os.environ.get("CLIENT_MAX_TRIES"))

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
        db.rpush(os.environ.get("IMAGE_QUEUE"), json.dumps(d))
        num_tries = 0
        while num_tries < CLIENT_MAX_TRIES:
            num_tries += 1

            output = db.get(k)

            if output is not None:
                output = output.decode("utf-8")
                data["detection"] = json.loads(output)

                db.delete(k)
                break
            time.sleep(float(os.environ.get("CLIENT_SLEEP")))

            data["success"] = True
        else:
            raise HTTPException(status_code=400, detail="Request failed after {} tries".format(CLIENT_MAX_TRIES))

    # Return the data dictionary as a JSON response
    return data