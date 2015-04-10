__author__ = 'en0'

from models.utils import _repr_from_keys


class GenericDocument(object):
    def __init__(self, json=None, document=None):
        self.__document__ = {}
        if document:
            self.__document__ = document
        elif json:
            self.__document__ = _repr_from_keys(
                json,
                self.__required_fields__,
                self.__optional_fields__
            )
        else:
            raise KeyError("Empty Document")


    @property
    def entity(self):
        return _repr_from_keys(
            self.__document__,
            fields=None,
            optional_fields=self.__public_fields__
        )

    @property
    def private_entity(self):
        _ret = _repr_from_keys(
            self.__document__,
            fields=self.__required_fields__,
            optional_fields=self.__optional_fields__
        )
        return _ret


def GenericDocumentFactory(namespace, fields):
    """ Create a RedisDocument class with the given fields

    The field argument has some structure.

    Example:
    [
        # Field Name    Required    Public
        ('field1',      True,       True),
        ('field2',      False,      True),
        ('field3',      True,       False),
    ]

    :param fields: Fields that this document holds.
    :return: A class that can create objects of this type.
    """

    _def = {
        '__document_namespace__': namespace,
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

        _doc_string = "Required field: {0}." if is_required else "Optional field: {0}."
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

    return type(namespace + '_doc', (GenericDocument,), _def)
