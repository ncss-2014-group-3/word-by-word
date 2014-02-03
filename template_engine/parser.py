from .PythonNode import PythonNode
from .GroupNode import GroupNode
from .JSONNode import JSONNode
from .TextNode import TextNode
from .ForNode import ForNode
from .IfNode import IfNode

TOKENS = {
    '{{': 'startvar',
    '}}': 'endvar',
    '{%': 'starttag',
    '%}': 'endtag',
    }


class ParseException(Exception):
    pass


def render(filename, context=None):
    with open(filename) as f:
        text = f.read()

    return render_string(text, context)


def render_string(string, context=None):
    context = context or {}

    # if it does not already have a value for errors
    # add [] as errors
    context.setdefault('errors', [])

    return Parser(string).expand(context)


class Parser:
    """ Parser(text) -> parser object

Creates a new Parser object from a string that can be expanded. """

    def __init__(self, text):
        """ p.__init__(text) initialises the Parser and stores in p. """
        self._tokens = []
        while text:
            minpos = len(text)
            mintype = None
            for k, v in TOKENS.items():
                pos = text.find(k)
                if pos >= 0:
                    if pos < minpos:
                        minpos = pos
                        mintype = k

            if minpos == 0:
                self._tokens.append(TOKENS[mintype])
                text = text[len(mintype):]

            else:
                self._tokens.append(text[:minpos])
                text = text[minpos:]

        self._length = len(self._tokens)
        self._upto = 0

    def end(self):
        return self._upto == self._length

    def peek(self):
        return None if self.end() else self._tokens[self._upto]

    def prev(self):
        self._upto -= 1

    def next(self):
        if not self.end():
            self._upto += 1

    def match(self, token, error=None):
        if error is None:
            error = token
        if self.peek() is None or self.peek().strip() != token:
            raise ParseException('No {}'.format(error))
        self.next()

    def split_tag(self):
        tag_contents = self.peek()
        if tag_contents is not None:
            keyword, *tag_contents = tag_contents.strip().split()
            return keyword, ' '.join(tag_contents)
        else:
            return None, None

    def expand(self, context=None):
        """
        p.expand(context = {}) -> str

        expanded form of the text given in the constructor.

        Context is a dictionary representing the variables in the local scope.
        """

        context = context or {}

        tree = self.parse_group()
        return tree.render(context)

    def parse_group(self):
        if self.end():
            return GroupNode([])

        child = None
        if self.peek() == 'startvar':
            self.next()
            child = self.parse_python()
            self.match('endvar')

        elif self.peek() == 'starttag':
            self.next()
            tag_contents = self.peek().strip()
            keyword = tag_contents.split()[0]
            if keyword == 'include':
                child = self.parse_include()
            elif keyword == 'if':
                child = self.parse_if()
            elif keyword == 'for':
                child = self.parse_for()
            elif keyword == 'json':
                child = self.parse_json()
            elif keyword in ('end', 'else'):
                self.prev()
                return GroupNode([])

            self.match('endtag')
        else:
            child = self.parse_text()

        group = self.parse_group()
        group.children = [child] + group.children

        return group

    def parse_for(self):
        keyword, for_condition = self.split_tag()

        self.next()
        self.match('endtag')
        group = self.parse_group()

        self.match('starttag', 'end for/else')

        keyword, tag_contents = self.split_tag()
        if keyword == 'else':
            self.match('else')
            self.match('endtag')
            else_group = self.parse_group()
            self.match('starttag')
        else:
            else_group = None

        self.match('end for')

        return ForNode(for_condition, group, else_group)

    def parse_if(self):
        keyword, predicate = self.split_tag()
        self.next()
        self.match('endtag')

        group = self.parse_group()
        self.match('starttag', 'end if/else')

        keyword, tag_contents = self.split_tag()

        if keyword == 'else':
            self.match('else')
            self.match('endtag')
            else_group = self.parse_group()
            self.match('starttag')
        else:
            else_group = None

        self.match('end if')

        return IfNode(predicate, group, else_group)

    def parse_python(self):
        if self.peek() == 'endvar':
            return PythonNode('')
        result = PythonNode(self.peek())
        self.next()
        return result

    def parse_text(self):
        result = TextNode(self.peek())
        self.next()
        return result

    def parse_json(self):
        keyword, json_data = self.split_tag()
        result = JSONNode(json_data)
        self.next()
        return result

    def parse_include(self):
        tag_contents = self.peek().strip()
        self.next()

        keyword, file_name, *context_args = tag_contents.split()
        context = {}
        if context_args:
            for c in context_args:
                k, v = c.split("=", maxsplit=1)
                context[k] = v

        if not context:
            return TextNode(
                render(file_name, context)
            )

        return IncludeNode(file_name, context)

from .IncludeNode import IncludeNode
