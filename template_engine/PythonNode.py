import html

class PythonNode:
    def __init__(self, code):
        self.code = code

    def render(self, context):
        try:
            result = eval(self.code, {}, context)
        except (NameError, SyntaxError):
            return ''
        else:
            return '' if result == None else html.escape(str(result))
    
    
    def __repr__(self):
        return "PythonNode({!r})".format(self.code)
    
