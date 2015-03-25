__author__ = 'en0'


class ApiException(Exception):
    def __init__(self, message, status_code=400, payload=None):
        super(Exception, self).__init__()
        self.message = "{0} - {1}".format(status_code, message)
        self.status_code = status_code

        _pl = dict(status_code=status_code)
        if payload:
            _pl.update(payload)
        self.payload = _pl

    def to_dict(self):
        rv = dict(self.payload or {})
        rv['message'] = self.message
        return rv
