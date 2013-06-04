from .snippets import *
from .employee import EmployeeApi
from .auth import AuthApi
from .payment import PaymentApi

@singleton
class Api:
    def employee(self, query):
        return EmployeeApi().execute(query)

    def auth(self, query):
        return AuthApi().execute(query)

    def payment(self, query):
        return PaymentApi().execute(query)

    def __init__(self):
        self.map = { 'employee': self.employee,
                     'auth':     self.auth,
                     'payment':  self.payment }

    def execute(self, query):
        method = query['method'].split('.', 2)
        module = method[0]
        if module in self.map:
            # Remove module prefix from method
            subquery = query.copy()
            subquery['method'] = method[1]
            # Execute method of some module
            return self.map[module](subquery)
        else:
            raise AssertionError('Unknown module of method')
