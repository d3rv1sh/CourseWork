
import json
from webob import Request, Response

from .api import Api

class ProxyApp:
    params_filter = ['method', 'id', 'login', 'password', 'token', 'method_id']

    def __call__(self, environ, start_response):
        req = Request(environ)
        req.charset = 'utf8'

        try:
            query = self.parse_request_params(req.params)
            data = Api().execute(query)
        except AssertionError as e:
            data = { 'error': e.args }

        json_data = json.dumps(data)
        response = Response(json_data, content_type='application/json')
        return response(environ, start_response)

    def parse_request_params(self, params):
        """
        Parse params of request
            Validates that param name are from whitelist
            Validates that params are not duplicated
            Validates that params are convertable to str
            Validates that method name is specified
        """
        data = {}
        for name, value in params.items():
            if name in self.params_filter:
                if name not in data:
                    data[name] = str(value)
                else:
                    raise AssertionError('Duplicated params in request')
            else:
                raise AssertionError('Some param name is not whitelisted')

        if 'method' not in data:
            raise AssertionError('Method name is not specified')
        return data

