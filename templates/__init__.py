#
# Params required for correct templates loading
#

import jinja2

JINJA_ENV = jinja2.Environment( loader     = jinja2.FileSystemLoader('templates'),
                                extensions = ['jinja2.ext.autoescape'], )

class Templates:
    @staticmethod
    def get(filename):
        return JINJA_ENV.get_template(filename)
