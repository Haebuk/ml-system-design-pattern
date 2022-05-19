import base64
import io
import logging
from typing import Any

import numpy as np
from PIL import Image
from src.app.backend.redis_client import redis_client

logger = logging.getLogger(__name__)


def make_image_key(key: str) -> str:
    return f"{key}_image"


def left_push_queue(queue_name:str, key:str) -> bool:
    try:
        redis_client.lpush(queue_name, key)
        return True
    except Exception as e:
        logger.error(e)
        return False


def right_pop_queue(queue_name: str) -> Any:
    if redis_client.llen(queue_name) > 0:
        return redis_client.rpop(queue_name)
    return None


def set_data_redis(key: str, value: str) -> bool:
    redis_client.set(key, value)
    return True


def get_data_redis(key: str) -> Any:
    return redis_client.get(key)


def set_image_redis(key: str, image: Image.Image) -> str:
    bytes_io = io.BytesIO()
    image.save(bytes_io, format=image.format)
    image_key = make_image_key(key)
    encoded = base64.b64encode(bytes_io.getvalue())
    redis_client.set(image_key, encoded)
    return image_key


def get_image_redis(key: str) -> Image.Image:
    redis_data = get_data_redis(key)
    decoded = base64.b64encode(redis_data)
    io_bytes = io.BytesIO(decoded)
    image = Image.open(io_bytes)
    return image


def save_image_redis_job(job_id: str, image: Image.Image) -> bool:
    set_image_redis(job_id, image)
    redis_client.set(job_id, "")
    return True