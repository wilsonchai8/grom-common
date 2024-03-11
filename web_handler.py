from tornado.web import RequestHandler, Application, HTTPError
from tornado.ioloop import IOLoop
import tornado.httpserver as httpserver
from tornado.escape import url_unescape
from .log_handler import logger, access_logger
import traceback
import json
from .exception_handler import *
from datetime import date, datetime
from .utils import JwtManager


class WebHandler(RequestHandler):

    def initialize(self):
        pass

    def prepare(self):
        try:
            if self.request.headers.get('Authorization'):
                auth_type, payload = self.request.headers.get('Authorization').split('')
            else:
                self.auth = self.cookies['auth'].value
                self.current_user = self.cookies['username'].value
                self.nickname = self.cookies['nickname'].value
                self.email = self.cookies['email'].value
                self.contact = self.cookies['contact'].value
                self.routes = self.cookies['routes'].value
                self.components = self.cookies['components'].value
                self.requests = self.cookies['requests'].value
                payload = self.auth
        except KeyError:
            raise AuthError('authentication failed')
        except Exception as e:
            raise e

        try:
            jm = JwtManager()
            jm.decode(payload)
        except Exception as e:
            raise AuthError(msg=str(e))

    def on_finish(self):
        access_logger.info('{} {} {} {} {} {}ms'.format(
            self.request.protocol,
            self._status_code,
            self.request.method,
            self.request.uri,
            '-' if not self.request.body else self.request.body.decode(
                'utf-8'),
            float(str(self.request.request_time()*1000)[0:5])))

    def write_error(self, status_code, **kwargs):
        msg = None
        if 'exc_info' in kwargs:
            if LoginError in kwargs.get('exc_info'):
                status_code = 401
            elif AuthError in kwargs.get('exc_info'):
                status_code = 401
            elif ForbiddenError in kwargs.get('exc_info'):
                status_code = 403
            msg = kwargs.get('exc_info')[1].args[0]
            code = kwargs.get('exc_info')[1].args[1]
            self.reply(msg, code, status_code)
        else:
            self.reply(self.reason, 1, status_code)

    def reply(self, msg=None, code=SUCCESS, status_code=200, **kwargs):
        res = {
            'code': code,
            'msg': MSGS.get(code) if not msg else msg,
            'payload': kwargs
        }
        res_formated = json.dumps(res, cls=JsonTimeEncoder)
        self.set_status(status_code)
        self.finish(res_formated)

    def log_exception(self, typ, value, tb):
        logger.error(traceback.format_exc())

    def get_request_query_json(self):
        ret = {}
        if self.request.arguments:
            for name, values in self.request.query_arguments.items():
                if len(values) == 1:
                    if values[0] != b'':
                        ret[name] = values[0].decode()
                else:
                    ret[name] = [i.decode() for i in values]
        return ret

    def get_request_body_json(self):
        ret = {}
        if self.request.body:
            try:
                data = json.loads(self.request.body.decode('utf-8'))
            except json.JSONDecodeError:
                raise ParamError('body json decode error')
            for name, values in data.items():
                ret[name] = values
        return ret


def get_loop():
    return IOLoop.current().asyncio_loop


class JsonTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)
