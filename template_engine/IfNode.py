class IfNode:
    def __init__(self, predicate, group):
        self.predicate = predicate
        self.group = group

    def render(self, context):
        condition = eval(self.predicate, {}, context)
        
        if condition:
            return self.group.render(context)
        else:
            return ''

    def __repr__(self):
        return 'IfNode({!r})'.format(self.children)
    
