class IfNode:
    def __init__(self, predicate, group_true, group_false = None):
        self.predicate = predicate
        self.group_true = group_true
        self.group_false = group_false

    def render(self, context):
        condition = eval(self.predicate, {}, context)
        if condition:
            return self.group_true.render(context)
        elif self.group_false is not None:
            return self.group_false.render(context)
        else:
            return ''

    def __repr__(self):
        return 'IfNode({!r})'.format(self.children)
    
