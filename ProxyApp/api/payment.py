from .snippets import *
from ..database import DataContext

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
                UPDATE employees
                SET payment_method_id = %s,
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