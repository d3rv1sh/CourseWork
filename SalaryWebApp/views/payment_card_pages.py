
from . import *
from ..proxy_api import proxy_api_call
from templates import Templates

class PaymentCardPages(LayoutedView):
    def render(self):
        params = { 'id': '1',
                   'token': '76c2a6725d80a164b38479290c842973896d9469d8e4598404885ab855c59c60' }
        data = proxy_api_call('employee.getPaymentMethods', params)

        context = {'cards': data['methods'] }

        card_select_template = Templates.get('payment_card_select.html')
        self.content = card_select_template.render(context)

        return super().render()