
from .snippets import *
from .auth import AuthApi
from ..database import DataContext

@singleton
class EmployeeApi:
    def get_personal_details(self, query, subject):
        # Params list validation
        check_whitelist(query, ['id'])
        check_mandatory(query, ['id'])

        # Params data validation
        data = { 'id': int_param(query['id']) }
        if subject['class'] == 'employee':
            if int(subject['id']) != data['id']:
                raise AssertionError('Access violation')
        elif subject['class'] == 'superuser':
            pass
        else:
            raise AssertionError('Access violation')

        # Drop query for security reasons
        query = None

        # SQL operations
        with DataContext() as db:
            cur = db.execute("""
                SELECT id, first_name, last_name
                FROM employees
                WHERE id = %s
            """, data['id'])

            res = cur.fetchone()
            if res is not None:
                data['first_name'] = res[1]
                data['last_name'] = res[2]
            else:
                raise AssertionError('Employee not found')
        return data

    def __init__(self):
        self.map = { 'getPersonalDetails': self.get_personal_details }

    def execute(self, query):
        method = query['method']
        if 'token' in query:
            token = strn_param(query['token'], 64)
        else:
            raise AssertionError('Auth token is missed')

        subject = AuthApi().private_check_token(token)

        if method in self.map:
            subquery = query.copy()
            del(subquery['method'])
            del(subquery['token'])
            # Execute mapped method
            return self.map[method](subquery, subject)
        else:
            raise AssertionError('Unknown method')