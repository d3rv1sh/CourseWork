from .snippets import *
from ..database import DataContext
from .auth import AuthApi

@singleton
class PaymentApi:
    def private_add_payment_method(self, employee_id, card_number):
        # SQL operations
        with DataContext() as db:
            cur = db.execute("""
                INSERT INTO payment_methods (employee_id, card_number)
                VALUES (%s, %s);
            """, (employee_id, card_number))
            try:
                db.commit()
            except Exception:
                raise AssertionError('Unable to add payment method')

            if cur is None:
                raise AssertionError('Unable to add payment method')

    def private_set_default_payment_method(self, employee_id, method_id):
        # SQL operations
        with DataContext() as db:
            cur = db.execute("""
                SELECT id
                FROM payment_methods
                WHERE id = %s AND employee_id = %s
                LIMIT 1;
            """, (method_id, employee_id))
            res = cur.fetchone()
            if res[0] != method_id:
                raise AssertionError('Access violation')

            cur = db.execute("""
                UPDATE employees
                SET payment_method_id = %s
                WHERE id = %s;
            """, (method_id, employee_id))
            try:
                db.commit()
            except Exception:
                raise AssertionError('Unable to set default payment method')

            if cur is None:
                raise AssertionError('Unable to set default payment method')

    def private_get_masked_payment_methods(self, employee_id):
        # SQL operations
        with DataContext() as db:
            cur = db.execute("""
                SELECT id, card_number
                FROM payment_methods
                WHERE employee_id = %s;
            """, employee_id)
            res = cur.fetchall()
            if res is not None:
                data = []
                for tup in res:
                    data.append( { 'id': tup[0],
                                   'card_number': mask_card_number(tup[1]) } )
                return data
            else:
                raise AssertionError('Token is not valid')

    def get_all_payment_methods(self, query,  subject):
        # Params list validation
        check_whitelist(query, [])

        # Params data validation
        if subject['class'] != 'paybot':
            raise AssertionError('Access violation')
        # Drop query for security reasons
        query = None

        data = { 'employee_cards': [] }
        # SQL operations
        with DataContext() as db:
            cur = db.execute("""
                SELECT employees.id, card_number
                FROM employees
                JOIN payment_methods ON payment_methods.id = employees.payment_method_id
            """)

            res = cur.fetchall()
            if res is not None:
                for tup in res:
                    data['employee_cards'].append( {'employee_id': tup[0], 'card_number': tup[1] } )
            else:
                raise AssertionError('No cards')
        return data

    def __init__(self):
        self.map = { 'getAllPaymentMethods': self.get_all_payment_methods, }

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