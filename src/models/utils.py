__author__ = 'en0'


def _repr_from_keys(json, fields, optional_fields):
    _ret = {}
    if fields:
        for field in fields:
            _ret[field] = json[field]

    if optional_fields:
        for field in optional_fields:
            _ret[field] = json.get(field)

    return _ret

