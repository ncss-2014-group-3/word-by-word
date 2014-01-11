class IfNode:
    def __init__(self, predicate, group_true, group_false = None):
        self.predicate = predicate
        self.group_true = group_true
        self.group_false = group_false

    def render(self, context):
        condition = eval(self.predicate, {}, context)
        
        if condition:
            return self.group_true.render(context)
        else:
            return self.group_false.render(context) if self.group_false is not None else ''

    def __repr__(self):
        return 'IfNode({!r})'.format(self.children)
    
