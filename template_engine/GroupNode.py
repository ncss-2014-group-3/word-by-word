from operator import methodcaller


class GroupNode(object):
    def __init__(self, children):
        self.children = children

    def render(self, context):
        caller = methodcaller('render', context)
        result = map(caller, self.children)

        return ''.join(result)

    def __repr__(self):
        return 'GroupNode({!r})'.format(self.children)
