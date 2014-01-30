from .PythonNode import PythonNode
from .GroupNode import GroupNode
from .JSONNode import JSONNode
from .TextNode import TextNode
from .ForNode import ForNode
from .IfNode import IfNode

TOKENS = {
    '{{' : 'startvar',
    '}}' : 'endvar',
    '{%' : 'starttag',
    '%}' : 'endtag',
    }


class ParseException(Exception):
    pass


def render(filename, context=None):
    context = context or {}

    parser_inst = Parser.from_file(filename)
    return parser_inst.expand(context)


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

    @classmethod
    def from_file(cls, file_name):
        with open(file_name) as f:
            text = f.read()
        return Parser(text)

    def expand(self, context={}):
        r""" p.expand(context = {}) -> str

expanded form of the text given in the constructor.

Context is a dictionary representing the variables in the local scope.

>>> Parser('Test {{ 3 * 9 }}').expand()
'Test 27'
>>> Parser('Test {{ var + 3 }}').expand({ 'var' : 9})
'Test 12'
>>> Parser('Test {{ var }}').expand({ 'var' : '<p> <!-- --> "\'\\/ &amp; & #? <!CDATA[[ &'})
'Test &lt;p&gt; &lt;!-- --&gt; &quot;&#x27;\\/ &amp;amp; &amp; #? &lt;!CDATA[[ &amp;'
>>> Parser('var * 9 = {{ var * 9 }} WORDS! {{ 6 * 9 - (var + 4)}}').expand({ 'var' : 1.4})
'var * 9 = 12.6 WORDS! 48.6'
>>> text = 'Test words {% if var == 1 %} The world is good {% end if %} '
>>> Parser(text).expand({'var' : 1})
'Test words  The world is good  '
>>> Parser(text).expand({'var' : 0})
'Test words  '
>>> Parser('{% hello').expand()
Traceback (most recent call last):
  ...
ParseException: No endtag
>>> Parser('{% if 1 == 1 %}hello').expand()
Traceback (most recent call last):
  ...
ParseException: No end if/else
>>> text = '{% if var >= 1%}{%if var == 1 %}var = 1, {% end if %}var >= 1{% end if %}'
>>> Parser(text).expand({ 'var' : 1})
'var = 1, var >= 1'
>>> Parser(text).expand({ 'var' : 2})
'var >= 1'
>>> Parser(text).expand({ 'var' : 0})
''
>>> Parser(text).expand({ 'var' : ''})
Traceback (most recent call last):
  ...
TypeError: unorderable types: str() >= int()
>>> Parser('Test {% for i in range(10) %} i = {{ i }} {% end for %}').expand()
'Test  i = 0  i = 1  i = 2  i = 3  i = 4  i = 5  i = 6  i = 7  i = 8  i = 9 '
>>> Parser('Test: {% for i in range(10) %}{% if i / 2 == int(i / 2) %}{{ i }} is divisible by two. {% end if %}{% end for %}').expand()
'Test: 0 is divisible by two. 2 is divisible by two. 4 is divisible by two. 6 is divisible by two. 8 is divisible by two. '
>>> Parser('{% for i in range(5) %} {{ i }}').expand()
Traceback (most recent call last):
  ...
ParseException: No end for/else
>>> Parser('{%for i in (\'dog\', \'cat\', \'frog\') %}{{ i }} {% end for %}').expand()
'dog cat frog '
>>> Parser('{% for i in range(9) %}{% for j in \'abcd\'%}{{ str(i) + j }},{%end for %}{% end for %}').expand()
'0a,0b,0c,0d,1a,1b,1c,1d,2a,2b,2c,2d,3a,3b,3c,3d,4a,4b,4c,4d,5a,5b,5c,5d,6a,6b,6c,6d,7a,7b,7c,7d,8a,8b,8c,8d,'
>>> Parser('{%if var == 1 %} var = 1 {% else%} var != 1{%end if %}').expand({'var':0})
' var != 1'
>>> Parser('{%if var == 1 %} var = 1 {% else%} var != 1{%end if %}').expand({'var':1})
' var = 1 '
>>> Parser('{% for i,e in enumerate("abcde") %}{{e}} is the {{i}}th letter, {%end for%}').expand()
'a is the 0th letter, b is the 1th letter, c is the 2th letter, d is the 3th letter, e is the 4th letter, '
>>> text = '{%for a in [i for i in range(10) if i == var] %} {{a}} == {{var}} {%else%}No numbers in 0..9 equal {{var}}{%end for%}'
>>> Parser(text).expand({'var':100})
'No numbers in 0..9 equal 100'
>>> Parser(text).expand({'var':5})
' 5 == 5 '
>>> Parser('{{[s for s in range(9) if s == var]}}').expand({'var':5})
'[5]'
>>> Parser('{%json {"bla":["a", "b"]}%}').expand()
'{"bla": ["a", "b"]}'
>>> #Parser("{% json {'word':'this', 'id':3, 'childern_ids':[1,2,4]} %}" ).expand()
>>> #'{"childern_ids": [1, 2, 4], "id": 3, "word": "this"}'
"""
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

if __name__ == '__main__':
    import doctest
    nFailed, nTests = doctest.testmod()
    if nFailed == 0:
        print('Passed')
