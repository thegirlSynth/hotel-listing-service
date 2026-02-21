import redis
import uuid
import json


r = redis.Redis(
    host='redis-10137.c12.us-east-1-4.ec2.cloud.redislabs.com',
    port=10137,
    decode_responses=True,
    username="default",
    password="TrDw48WTAC1aVYD3bGrYmDewItTHAoKF",
)


def store_search_session(hotel_ids):
    session_id = str(uuid.uuid4())
    r.setex(f"session:{session_id}", 1800, json.dumps(hotel_ids))  # 30 mins expiry
    return session_id

def get_cached_hotel_ids(session_id):
    data = r.get(f"session:{session_id}")
    if not data:
        return []
    return json.loads(data)
