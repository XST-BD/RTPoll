from datetime import datetime, timedelta, timezone
from jose import jwt
from pathlib import Path 
import uuid

from app.setup.cache import redis_client 
from app.setup.vars import SECRET_KEY

ALGORITHM = "HS256"


def create_token():
    voter_id = str(uuid.uuid4())

    payload = {
        "vid": voter_id,
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(days=7)
    }

    token = jwt.encode(payload, key=str(SECRET_KEY), algorithm=ALGORITHM)
    return token


def verify_token(token: str):
    try:
        payload = jwt.decode(token, key=str(SECRET_KEY), algorithms=[ALGORITHM])
        return payload["vid"]
    except:
        return None


class LuaScript:
    def __init__(self, redis, path):
        self.redis = redis
        self.script = Path(path).read_text()
        self.sha = self.redis.script_load(self.script)

    def execute(self, keys, args):
        from redis.exceptions import NoScriptError
        try:
            return self.redis.evalsha(self.sha, len(keys), *keys, *args)
        except NoScriptError:
            self.sha = self.redis.script_load(self.script)
            return self.redis.evalsha(self.sha, len(keys), *keys, *args)
        

vote_script = LuaScript(redis_client, 'lua/vote.lua')