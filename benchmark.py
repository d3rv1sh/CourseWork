
import time
from ProxyApp.database import DataContext
from SalaryWebApp.proxy_api import proxy_api_call

def test1_sql(n):
    t1 = time.time()
    for i in range(n):
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
    t2 = time.time()
    print('SQL took {0:3f} secs.'.format(t2 - t1))

def test1_proxy(n):
    t1 = time.time()
    for i in range(n):
        params = { 'token': 'b1555127084a674fa386d2ec12d02cb57881dde57080d8cea7fd04538c1d63c8' }
        data = proxy_api_call('payment.getAllPaymentMethods', params)
        if 'error' in data:
            raise AssertionError(data['error'])
    t2 = time.time()
    print('Proxified queries took {0:3f} secs.'.format(t2 - t1))

def main():
    test1_sql(1000)
    test1_proxy(1000)

if __name__ == '__main__':
    main()