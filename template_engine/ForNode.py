class ForNode:
    def __init__(self, for_condition, group):
        self.for_condition = for_condition
        self.group = group

    def render(self, context):
        var, iterator = self.for_condition.split(' in ')
        iterator = eval(iterator, {}, context)

        result = ''
        for item in iterator:
            context[var] = item
            result += self.group.render(context)
        
        return result
        
    def __repr__(self):
        return 'IfNode({!r})'.format(self.children)
    
