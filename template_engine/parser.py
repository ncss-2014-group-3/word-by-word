import re
from GroupNode import GroupNode
from PythonNode import PythonNode
from TextNode import TextNode
from IfNode import IfNode

TOKENS = {
    '{{' : 'startvar',
    '}}' : 'endvar',
    '{%' : 'starttag',
    '%}' : 'endtag',
    }

class ParseException(Exception):
    pass


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

    def split_tag(self):
        tag_contents = self.peek().strip()
        keyword, tag_contents = tag_contents.split(sep = None, maxsplit = 1)
        return keyword, tag_contents
        
    def expand(self, context={}):
        """ p.expand(context = {}) -> str

expanded form of the text given in the constructor.

Context is a dictionary representing the variables in the local scope.

>>> Parser('Test {{ 3 * 9 }}').expand()
'Test 27'
>>> Parser('Test {{ var + 3 }}').expand({ 'var' : 9})
'Test 12'
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
ParseException: No end tag
>>> Parser('{% if 1 == 1 %}hello').expand()
Traceback (most recent call last):
  ...
ParseException: No end if
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
            if self.peek() != 'endvar':
                raise ParseException('No closing "}}"')
            self.next()
            
        elif self.peek() == 'starttag':
            self.next()
            tag_contents = self.peek().strip()
            keyword = tag_contents.split()[0]
            #import pdb; pdb.set_trace()
            if keyword == 'include':
                child = self.parse_include()
            elif keyword == 'if':
                child = self.parse_if()
            elif keyword == 'end':
                self.prev()
                return GroupNode([])
                
            if self.peek() != 'endtag':
                raise ParseException('No end tag')
                
            self.next()
        else:
            child = self.parse_text()

        group = self.parse_group()
        group.children = [child] + group.children

        return group


    def parse_if(self):
        keyword, predicate = self.split_tag()
        

        self.next()
        if self.peek() != 'endtag':
            raise ParseException('No end tag')
        self.next()
        group = self.parse_group()

        if self.peek() != 'starttag':
            raise ParseException('No end if')

        self.next()
        
        keyword, tag_contents = self.split_tag()

        if keyword != 'end' or tag_contents != 'if':
            raise ParseException('No end if')
        self.next()
        
        return IfNode(predicate, group)

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

    def parse_include(self):
        tag_contents = self.peek().strip()
        keyword, tag_contents = tag_contents.split(sep = None, maxsplit = 1)
        
        with open(tag_contents) as f:
            text = f.read()
            result = Parser(text).expand()

        self.next()
        return TextNode(result)


if __name__ == '__main__':
    import doctest
    nFailed, nTests = doctest.testmod()
    if nFailed == 0:
        print('Passed')
