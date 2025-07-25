import redis
import uuid
import json


r = redis.Redis(
    host='redis-12465.c11.us-east-1-3.ec2.redns.redis-cloud.com',
    port=12465,
    decode_responses=True,
    username="default",
    password="3CKySbhvbUODLzZx4shl8bjZLzwd8VuT",
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
