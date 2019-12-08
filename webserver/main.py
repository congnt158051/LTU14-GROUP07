import time

import redis
from fastapi import FastAPI, File, HTTPException

app = FastAPI()
cache = redis.StrictRedis(host='redis')


def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


@app.get("/")
def hello():
    count = get_hit_count()
    return 'Hello World! I have been seen {} times.\n'.format(count)