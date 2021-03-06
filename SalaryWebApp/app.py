
import os
from webob import Request, Response
from webob.exc import HTTPTemporaryRedirect
from .proxy_api import proxy_api_call
from .views.index_pages import IndexPages
from .views.payment_card_pages import PaymentCardPages

class SampleApp:
    def __init__(self, storage_dir):
        self.storage_dir = os.path.abspath(os.path.normpath(storage_dir))

    def __call__(self, environ, start_response):
        """
        Главный обработчик HTTP событий
        """
        req = Request(environ)

        # Список вторичных обработчиков запросов
        # Для простоты регулярные выражения не используются
        routes = { '/cw': self.index,
                   '/cw/login': self.login,
                   '/cw/logout': self.logout,
                   '/cw/cards': self.cards,
                   '/cw/set_payment_card': self.set_payment_card,
                   '/cw/paybot/cards': self.paybot_cards }

        # Поиск вторичного обработчика события
        if req.path_info in routes:
            handler = routes[req.path_info]
        else:
            response = Response('Not found', status=404)
            return response(environ, start_response)

        # Проверка наличия авторизационного токена
        token = None
        if req.cookies.get('token'):
            token = req.cookies['token']

        # Вызов вторичного обработчика событий
        page_tup = {}
        try:
            page_tup = handler(req, token)
            page = page_tup['page']
        except AssertionError as e:
            page = 'Error {0}'.format(str(e.args))

        # Подготовка HTTP ответа
        response = Response(page, content_type='text/html')
        if 'redirect_to' in page_tup:
            response = req.get_response(HTTPTemporaryRedirect(location=page_tup['redirect_to']))
            response.text = page
        if 'set_cookies' in page_tup:
            for cookie in page_tup['set_cookies']:
                response.set_cookie(cookie[0], cookie[1], httponly=True)
        return response(environ, start_response)

    def index(self, req, token=None):
        """
        Обработчик URL главной страницы
        """
        view = IndexPages()
        user_name = None
        # Поиск имени и фамилии по токену
        if token is not None:
            # proxy_api_call вызывает методы нашего проксирующего модуля
            data = proxy_api_call('employee.getPersonalDetails', { 'token': token })
            if 'first_name' in data:
                user_name = '{0} {1}'.format(data['first_name'], data['last_name'])

        # Рендеринг страницы
        view.variant = 'index'
        view.data_context = { 'user_name': user_name }
        return {'page': view.render()}

    def cards(self, req, token=None):
        """
        Список банковских карт сотрудника
        """
        params = { 'token': token }
        data = proxy_api_call('employee.getPaymentMethods', params)
        if 'error' in data:
            raise AssertionError(data['error'])

        view = PaymentCardPages()
        view.data_context = { 'cards': data['methods'] }
        return {'page': view.render()}

    def paybot_cards(self, req, token=None):
        """
        Показывает банковские карты с привелегиями платежного робота
        """
        # В тестовом случае используем заранее заданный токен
        # К тому же, в реальности токен платежного робота никак
        # не может быть связан с данными получаемыми из браузера
        params = { 'token': 'b1555127084a674fa386d2ec12d02cb57881dde57080d8cea7fd04538c1d63c8' }
        data = proxy_api_call('payment.getAllPaymentMethods', params)
        if 'error' in data:
            raise AssertionError(data['error'])

        view = PaymentCardPages()
        view.data_context = { 'cards': data['employee_cards'] }
        view.variant = 'paybot'
        return {'page': view.render()}

    def set_payment_card(self, req, token=None):
        """
        Устанавливает банковскую карту по умолчанию
        """
        try:
            params = { 'token': token, 'method_id': req.params['card_id'] }
        except Exception:
            raise AssertionError('No enough params')

        data = proxy_api_call('employee.setPaymentMethod', params)
        if 'error' in data:
            raise AssertionError(data['error'])

        params = { 'token': token }
        data = proxy_api_call('employee.getPaymentMethods', params)
        if 'error' in data:
            raise AssertionError(data['error'])

        view = PaymentCardPages()
        view.data_context = { 'cards': data['methods'] }
        view.variant = 'success'
        return {'page': view.render()}

    def login(self, req, token=None):
        """
        Авторизация
        """
        try:
            params = { 'login': req.params['login'],
                       'password': req.params['password'] }
        except Exception:
            raise AssertionError('Someparams are invalid')
        data = proxy_api_call('auth.getEmployeeToken', params)
        if 'error' in data:
            raise AssertionError(data['error'])

        res = { 'set_cookies': [('token', data['token'])],
                'redirect_to': 'https://nz.acmer.me/cw',
                'page': 'Succesful login'}
        return res

    def logout(self, req, token=None):
        """
        Отмена авторизации
        """
        res = { 'set_cookies': [('token', 'logged_out')],
                'redirect_to': 'https://nz.acmer.me/cw',
                'page': 'Succesful logout'}
        return res




