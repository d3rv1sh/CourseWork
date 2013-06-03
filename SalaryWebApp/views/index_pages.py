
from . import *
from templates import Templates

class IndexPages(LayoutedView):
    def render(self):
        self.pages = { 'index': 'index.html' }
        if ('user_name' in self.data_context) and \
           (self.data_context['user_name'] is not None):
            self.greetings = 'Hello! You\'ve logged in as {0}'.format(self.data_context['user_name'])
        else:
            self.data_context['login_form'] = Templates.get('login_form.html').render()

        self.index(self.pages[self.variant])
        return super().render()

    def index(self, template_file):
        template = Templates.get(template_file)
        self.content = template.render(self.data_context)
