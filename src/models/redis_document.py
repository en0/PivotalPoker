__author__ = 'en0'

from uuid import uuid4
import pickle
from models.utils import _repr_from_keys


class RedisDocument(object):
    def __init__(self, uuid=None, db=None):
        self.__document__ = {}
        self.__uuid__ = str(uuid)
        self.__is_dirty__ = False
        self.__db__ = db

    def save(self):
        if self.__is_dirty__:
            # Pretty strait forward.
            _set_document(
                self.__document_namespace__,
                self.__uuid__,
                self.__serializer__.dumps(self.__document__),
                self.__db__
            )
            return True
        return False

    def delete(self):
        self.__db__.hdel(self.__document_namespace__, self.__uuid__)

    @property
    def uuid(self):
        return self.__uuid__

    @property
    def entity(self):
        return _repr_from_keys(
            self.__document__,
            fields=None,
            optional_fields=self.__public_fields__
        )

    @property
    def private_entity(self):
        return _repr_from_keys(
            self.__document__,
            fields=self.__required_fields__,
            optional_fields=self.__optional_fields__
        )

    @classmethod
    def create(cls, json, db):
        _ret = cls(str(uuid4()), db=db)
        _ret.__is_dirty__ = True
        _ret.__document__ = _repr_from_keys(
            json,
            cls.__required_fields__,
            cls.__optional_fields__
        )
        return _ret

    @classmethod
    def load(cls, uuid, db):
        _ret = cls(uuid, db=db)
        dat = _get_document(cls.__document_namespace__, uuid, db)

        if not dat:
            return None

        _ret.__is_dirty__ = False
        _ret.__document__ = _repr_from_keys(
            json=cls.__serializer__.loads(dat),
            fields=None,
            optional_fields=cls.__required_fields__ + cls.__optional_fields__
        )
        return _ret

    @classmethod
    def exists(cls, uuid, db):
        dat = _get_document(cls.__document_namespace__, uuid, db)
        if not dat:
            return False
        return True

    @classmethod
    def get_document_ids(cls, db):
        return _get_uuids(cls.__document_namespace__, db)


def _format_key(namespace, uuid):
    return "{0}:{1}".format(namespace, uuid)


def _get_document(namespace, uuid, db):
    key = _format_key(namespace, uuid)
    return db.get(key)


def _get_uuids(namespace, db):
    _keys = db.keys("{0}:*".format(namespace))
    _key_set = set()
    for _key in _keys:
        _key_split = _key.split(':')
        if len(_key_split) > 1:
            _key_set.add(_key_split[1])

    return [x for x in _key_set]


def _set_document(namespace, uuid, value, db):
    key = _format_key(namespace, uuid)
    return db.set(key, value)


def RedisDocumentFactory(namespace, fields, serializer=None):

    _def = {
        '__document_namespace__': namespace,
        '__serializer__': serializer or pickle,
        '__required_fields__': [],
        '__optional_fields__': [],
        '__public_fields__': [],
    }

    def _property_for(field, is_required, is_public):
        def __getter(self):
            return self.__document__.get(field)

        def __setter(self, value):
            self.__document__[field] = value
            self.__is_dirty__ = True

        def __del(self):
            if is_required:
                raise TypeError("This field is required.")
            del self.__document__[field]
            self.__is_dirty__ = True

        if is_required:
            _doc_string = "Required field: {0}."
        else:
            _doc_string = "Optional field: {0}."

        _doc_string += " This field is public." if is_public else ""

        return property(__getter, __setter, __del, _doc_string.format(field))

    for _field, _required, _public in fields:
        if _required:
            _def['__required_fields__'].append(_field)
        else:
            _def['__optional_fields__'].append(_field)

        if _public:
            _def['__public_fields__'].append(_field)

        _def[_field] = _property_for(_field, _required, _public)

    return type(namespace + '_doc', (RedisDocument,), _def)
