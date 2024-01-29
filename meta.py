import abc
import base64
import json
from .exception_handler import ParamError
from .log_handler import logger
from datetime import date, datetime

__all__ = (
    'ConfigMetaClass',
    'CouldBlank',
    'NonBlank',
    'MustInteger',
    'MustTimeStamp',
    'MustDateTime',
    'MustJson',
    'MaybeBool',
    'MustString',
    'Base64Decode',
)

class ConfigMetaClass:
    
    def __init__(self, *args, **kwargs) -> None:
        logger.info('{}, {}'.format(self.__class__.__name__, kwargs))


class UserProperty: 
    __counter = 0

    def __init__(self, property_name=None) -> None:
        cls = self.__class__
        _index = cls.__counter
        if property_name:
            _prefix = property_name
        else:
            _prefix = cls.__name__
        self._property_name = '#{}_{}'.format(_index, _prefix)
        cls.__counter += 1

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return getattr(instance, self._property_name)

    def __set__(self, instance, value):
        setattr(instance, self._property_name, value)


class Validated(abc.ABC, UserProperty): 

    def __set__(self, instance, value):
        value = self.validate(instance, value)
        super().__set__(instance, value) 

    @abc.abstractmethod
    def validate(self, instance, value): 
        """return validated value or raise ValueError"""


class CouldBlank(Validated):
    
    def validate(self, instance, value):
        return value

        
class NonBlank(Validated):
    
    def validate(self, instance, value):
        if not value:
            raise ParamError(msg='{} can not be null'.format(self._property_name))
        return value


class MustInteger(Validated):
    
    def validate(self, instance, value):
        try:
            return int(value)
        except Exception:
            raise ParamError(msg='{} must be integer'.format(self._property_name))


class MustString(Validated):
    
    def validate(self, instance, value):
        try:
            if value is None: value = ''
            return str(value)
        except Exception:
            raise ParamError(msg='{} must be string'.format(self._property_name))


class MustJson(Validated):
    
    def validate(self, instance, value):
        try:
            return json.dumps(value, cls=JsonTimeEncoder)
        except Exception:
            raise ParamError(msg='{} must be json'.format(self._property_name))


class MustTimeStamp(Validated):
    
    def validate(self, instance, value):
        try:
            return datetime.fromtimestamp(value)
        except Exception:
            raise ParamError(msg='{} must be timestamp'.format(self._property_name))


class MustDateTime(Validated):

    def validate(self, instance, value):
        try:
            if not isinstance(value, datetime):
                raise ParamError(msg='{} must be datetime'.format(self._property_name))
            return value
        except Exception:
            return None


class MaybeBool(Validated):
    
    def validate(self, instance, value):
        try:
            if value == 0:
                return False
            if value == 1:
                return True
            if not isinstance(value, bool):
                assert value.lower() in ('true', 'false')
                value = eval('{}{}'.format(value[0].upper(), value[1:].lower()))
            assert isinstance(value, bool)
            return value
        except Exception:
            return None


class Base64Decode(Validated):
    
    def validate(self, instance, value):
        try:
            return str(base64.b64decode(value), encoding='utf8')
        except Exception:
            raise ParamError(msg='{} base64 transition error'.format(self._property_name))

            
class JsonTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)
