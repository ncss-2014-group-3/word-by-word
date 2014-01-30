class TextNode:
    def __init__(self, content):
        self.content = content

    def render(self, context):
        return self.content

    def __repr__(self):
        return 'TextNode({!r})'.format(self.content)
