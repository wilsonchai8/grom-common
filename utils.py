import hashlib
import jwt
import time
import datetime
import json


class Singleton(type):
    def __init__(self, *args, **kwargs):
        self.__instance = None
        super().__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        if self.__instance is None:
            self.__instance = super().__call__(*args, **kwargs)
        return self.__instance


def get_md5(data, bit=32):
    return hashlib.md5(data.encode('utf-8')).hexdigest() if bit == 32 else hashlib.md5(data.encode('utf-8')).hexdigest()[8:-8]


class JwtManager:

    def __init__(self):
        self.keyword = 'My life for the horde!!!'
        self.headers = {
            "alg": "HS256",
            "typ": "JWT"
        }

    def encode(self, payload, expire=43200):
        if expire != 0:
            payload.update({
                'exp': int(time.time() + expire)
            })
        return jwt.encode(
            payload=payload,
            key=self.keyword,
            algorithm='HS256',
            headers=self.headers).decode('utf-8')

    def decode(self, payload):
        payload = jwt.decode(payload, self.keyword, True, algorithm='HS256')
        return payload


class JsonTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)
