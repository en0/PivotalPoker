__author__ = 'en0'


from flask import jsonify
from flask.views import MethodView


class ResourceBase(MethodView):
    def dispatch_request(self, *args, **kwargs):
        result = super(ResourceBase, self).dispatch_request(*args, **kwargs)
        if type(result) != tuple:
            _dict = result
            headers = {}
            status = 200
        elif len(result) == 2:
            _dict, status = result
            headers = {}
        elif len(result) == 3:
            _dict, status, headers = result

        body = jsonify(_dict) if _dict else ""

        return body, status, headers


def register_route(view, app):
    _uri = view.__uri__
    _methods = view.__method_hints__

    if hasattr(view, '__pk__'):
        _pk_uri = "{0}<{2}:{1}>".format(_uri, view.__pk__, view.__pk_type__)
    else:
        _pk_uri = _uri

    view_fn = view.as_view("{0}_view".format(view.__name__.lower()))

    if 'GET' in _methods:
        if hasattr(view, '__pk__'):
            app.add_url_rule(_uri, defaults={view.__pk__: None}, view_func=view_fn, methods=['GET'])
            print("Register:", _uri, ['GET'])
        app.add_url_rule(_pk_uri, view_func=view_fn, methods=['GET'])
        print("Register:", _pk_uri, ['GET'])

    if 'PUT' in _methods:
        app.add_url_rule(_pk_uri, view_func=view_fn, methods=['PUT'])
        print("Register:", _pk_uri, ['PUT'])

    if 'POST' in _methods:
        app.add_url_rule(_uri, view_func=view_fn, methods=['POST'])
        print("Register:", _uri, ['POST'])

    if 'DELETE' in _methods:
        app.add_url_rule(_pk_uri, view_func=view_fn, methods=['DELETE'])
        print("Register:", _pk_uri, ['DELETE'])
