"""Redis config.

Contains setting:
- Auto decode
"""
from redis import Redis


redis_client = Redis(
    host='localhost',
    port=6379,
    db=0,
    decode_responses=True
)
