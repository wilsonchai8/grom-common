from .const import *


class ParamError(Exception):
    def __init__(self, msg="", code=PARAM_ERROR):
        msg = '{}： {}'.format(MSGS[PARAM_ERROR], msg)
        super().__init__(msg, code)

class LoginError(Exception):
    def __init__(self, msg="", code=LOGIN_ERROR):
        msg = '{}： {}'.format(MSGS[LOGIN_ERROR], msg)
        super().__init__(msg, code)

class AuthError(Exception):
    def __init__(self, msg="", code=AUTH_ERROR):
        msg = '{}： {}'.format(MSGS[AUTH_ERROR], msg)
        super().__init__(msg, code)

class ForbiddenError(Exception):
    def __init__(self, msg="", code=FORBIDDEN_ERROR):
        msg = '{}： {}'.format(MSGS[FORBIDDEN_ERROR], msg)
        super().__init__(msg, code)
        
class StateError(Exception):
    def __init__(self, msg="", code=STATE_ERROR):
        msg = '{}： {}'.format(MSGS[STATE_ERROR], msg)
        super().__init__(msg, code)

class RunError(Exception):
    def __init__(self, msg="", code=RUN_ERROR):
        msg = '{}： {}'.format(MSGS[RUN_ERROR], msg)
        super().__init__(msg, code)

class MysqlError(Exception):
    def __init__(self, msg="", code=MYSQL_ERROR):
        msg = '{}： {}'.format(MSGS[MYSQL_ERROR], msg)
        super().__init__(msg, code)
