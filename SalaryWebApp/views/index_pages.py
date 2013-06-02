
from . import *
from ..database import AppData

class IndexPages(LayoutedView):
    def render(self):
        with AppData() as db:
            cur = db.execute('SELECT VERSION()')
            ver = cur.fetchone()
            self.content = 'MySQL version: {0}'.format(ver)

        return super().render()
