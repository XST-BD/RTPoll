from datetime import datetime, timedelta, timezone
from jose import jwt
from pathlib import Path 
import uuid

from app.setup.cache import redis_client 
from app.setup.vars import SECRET_KEY

ALGORITHM = "HS256"


def create_token(role: str):
    voter_id = str(uuid.uuid4())

    payload = {
        "role": role,
        "vid": voter_id,
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(days=3)
    }

    token = jwt.encode(payload, key=str(SECRET_KEY), algorithm=ALGORITHM)
    return token


def verify_token(token: str):
    try:
        payload = jwt.decode(token, key=str(SECRET_KEY), algorithms=[ALGORITHM])
        return payload["vid"], payload["role"]
    except:
        return None, None

class LuaScript:
    def __init__(self, redis, path):
        self.redis = redis
        self.script = Path(path).read_text()
        self.sha = None

    async def execute(self, keys, args):
        if self.sha is None:
            self.sha = await self.redis.script_load(self.script)
        from redis.exceptions import NoScriptError
        try:
            return await self.redis.evalsha(self.sha, len(keys), *keys, *args)
        except NoScriptError:
            self.sha = self.redis.script_load(self.script)
            return await self.redis.evalsha(self.sha, len(keys), *keys, *args)
        

vote_script = LuaScript(redis_client, 'vote.lua')