from .snippets import *
from ..database import DataContext

@singleton
class AuthApi:
    def get_employee_token(self, query):
        # Params list validation
        check_whitelist(query, ['login', 'password'])
        check_mandatory(query, ['login', 'password'])

        # Params data validation
        data = { 'login': strn_param(query['login'], 32) }
        passwd = strn_param(query['password'], 64)

        # Drop query for security reasons
        query = None

        # SQL operations
        with DataContext() as db:
            cur = db.execute("""
                SELECT employee_id, passwd_hash, passwd_salt
                FROM employee_logins
                WHERE login = %s
            """, data['login'])

            res = cur.fetchone()
            if res is not None:
                data['id'] = res[0]
                passwd_hash = res[1]
                passwd_salt = res[2]
                expected_hash = hash_password(passwd, passwd_salt)
                #print (expected_hash)
                if passwd_hash == expected_hash:
                    token = self.private_authorize_token('employee', data['id'])
                    data = { 'token': token }
                else:
                    raise AssertionError('Incorrect password')
            else:
                raise AssertionError('Login not found')
        return data

    def private_authorize_token(self, subject_class, subject_id=None):
        token = generate_token()
        with DataContext() as db:
            cur = db.execute("""
                INSERT INTO auth_tokens (subject_class, subject_id, token, valid_from, valid_until)
                VALUES (%s, %s, %s, (NOW()), (NOW() + INTERVAL 720 MINUTE));
            """, (subject_class, subject_id, token))
            try:
                db.commit()
            except Exception:
                raise AssertionError('Unable to authorize token')

            if cur is None:
                raise AssertionError('Unable to authorize token')
        return token

    def private_check_token(self, token):
        with DataContext() as db:
            cur = db.execute("""
                SELECT subject_class, subject_id
                FROM auth_tokens
                WHERE token = %s AND valid_until > (NOW())
            """, token)
            res = cur.fetchone()
            if res is not None:
                data = { 'class': res[0],
                         'id': res[1] }
                return data
            else:
                raise AssertionError('Token is not valid')


    def __init__(self):
        self.map = { 'getEmployeeToken': self.get_employee_token }

    def execute(self, query):
        method = query['method']
        if method in self.map:
            subquery = query.copy()
            del(subquery['method'])
            # Execute mapped method
            return self.map[method](subquery)
        else:
            raise AssertionError('Unknown method')
