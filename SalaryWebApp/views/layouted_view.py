
from templates import Templates

class LayoutedView :
    def __init__(self):
        self.title = 'Default title'
        self.content = 'Default content'

    def render(self):
        template = Templates.get('layout.html')
        context = {'title':   self.title,
                   'content': self.content, }
        page = template.render(context)
        return page
