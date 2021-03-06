
from . import *
from templates import Templates

class PaymentCardPages(LayoutedView):
    def render(self):
        card_select_template = Templates.get('payment_card_select.html')
        if self.variant == 'success':
            self.data_context['form_message'] = 'Default payment method is successfully set'
            self.content = card_select_template.render(self.data_context)
        elif self.variant == 'paybot':
            cards_list_template = Templates.get('payment_cards_list.html')
            self.content = cards_list_template.render(self.data_context)
        else:
            self.content = card_select_template.render(self.data_context)
        return super().render()

    def __init__(self):
        super().__init__()
        self.data_context = {}
