import html
import json

class JSONNode:
    def __init__(self, code):
        self.code = code

    def render(self, context):
        result = eval(self.code, context)
        return '' if result == None else json.dumps(result)
    
    
    def __repr__(self):
        return "JSONNode({!r})".format(self.code)
    
