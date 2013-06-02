
import os
from webob import Request, Response

from .views.index_pages import IndexPages

class SampleApp:
    def __init__(self, storage_dir):
        self.storage_dir = os.path.abspath(os.path.normpath(storage_dir))

    def __call__(self, environ, start_response):
        req = Request(environ)
        view = IndexPages()
        page = view.render()
        response = Response(page, content_type='text/html')
        return response(environ, start_response)

