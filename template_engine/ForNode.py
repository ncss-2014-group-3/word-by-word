class ForNode:
    def __init__(self, for_condition, group, else_group=None):
        self.for_condition = for_condition
        self.group = group
        self.else_group = else_group

    def render(self, context):
        var, iterator = self.for_condition.split(' in ', maxsplit=1)
        import pdb; pdb.set_trace()
        iterator = eval(iterator, {}, context)

        result = ''
        atLeast1 = False
        name = '__item'
        while name in context: name = '_'+ name
        for item in iterator:
            exec('{} = {}'.format(var, name), {name:item}, context)
            result += self.group.render(context)
            atLeast1 = True
        if not atLeast1 and self.else_group is not None:
            result += self.else_group.render(context)
        if name in context:
            del context[name]
        return result
        
    def __repr__(self):
        return 'IfNode({!r})'.format(self.children)
    
