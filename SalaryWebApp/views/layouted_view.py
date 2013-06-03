
from templates import Templates

class LayoutedView :
    def __init__(self):
        self.title = 'Default title'
        self.greetings = ''
        self.content = 'Default content'
        self.variant = ''
        self.data_context = {}

    def render(self):
        template = Templates.get('layout.html')
        self.data_context['title'] = self.title
        self.data_context['greetings'] = self.greetings
        self.data_context['content'] = self.content
        page = template.render(self.data_context)
        return page
