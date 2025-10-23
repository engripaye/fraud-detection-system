import redis
import json
from typing import Dict


class RedisFeatureStore:
    def __init__(self, host="redis", port=6379, db=0):
        self.client = redis.Redis(host=host, port=port, db=db, decode_responses=True)

    def upset_user_features(self, user_id: str, features: Dict):
        self.client.hset("user_features", user_id, json.dumps(features))

    def get_user_features(self, user_id: str):
        data = self.client.hget("user_features", user_id)
        if data:
            return json.loads(data)
        return ()