
import os
from webob import Request, Response

from .views.index_pages import IndexPages
from .views.payment_card_pages import PaymentCardPages

class SampleApp:
    def __init__(self, storage_dir):
        self.storage_dir = os.path.abspath(os.path.normpath(storage_dir))

    def __call__(self, environ, start_response):
        req = Request(environ)
        routes = { '/cw/cards': self.cards }
        try:
            page = routes[req.path_info](req)
        except KeyError or AssertionError:
            page = 'Error'
        response = Response(page, content_type='text/html')
        return response(environ, start_response)

    def cards(self, req):
        view = PaymentCardPages()
        return view.render()


