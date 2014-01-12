class ForNode:
    def __init__(self, for_condition, group, else_group=None):
        self.for_condition = for_condition
        self.group = group
        self.else_group = else_group

    def render(self, context):
        var, iterator = self.for_condition.split(' in ', maxsplit=1)
        iterator = eval(iterator, {}, context)

        result = ''
        for item in iterator:
            exec('{} = {}'.format(var, repr(item)), {}, context)
            result += self.group.render(context)
        else:
            if self.else_group is not None:
                result += self.else_group.render(context)
        return result
        
    def __repr__(self):
        return 'IfNode({!r})'.format(self.children)
    
