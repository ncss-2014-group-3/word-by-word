class GroupNode(object):
    def __init__(self, children):
        self.children = children

    def render(self, context):
        result = ''
        for child in self.children:
            result += child.render(context)
        return result

    def __repr__(self):
        return 'GroupNode({!r})'.format(self.children)
