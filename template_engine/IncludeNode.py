from .parser import render


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

        return render(self.file_name, resolve_context)

    def __repr__(self):
        return "IncludeNode({!r}, {!r})".format(self.file_name, self.context)
