import html
#from parser import Parser

class IncludeNode:
    def __init__(self, file_name, context):
        self.file_name = file_name
        self.context = context

    def render(self, context):
        resolve_context = {}
        for k, v in self.context.items():
            try:
                resolve_context[k] = eval(v, {}, context)
            except (NameError, SyntaxError):
                return ''
        result = Parser.from_file(self.file_name).expand(resolve_context)
        return result    
    
    def __repr__(self):
        return "IncludeNode({!r}, {!r})".format(self.file_name, self.context)
