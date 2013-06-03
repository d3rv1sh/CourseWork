
from . import *
from ..proxy_api import proxy_api_call

class IndexPages(LayoutedView):
    def render(self):
        params = { 'id': '1',
                   'token': '76c2a6725d80a164b38479290c842973896d9469d8e4598404885ab855c59c60' }
        json_data = proxy_api_call('employee.getPaymentMethods', params)
        self.content = json_data

        return super().render()
