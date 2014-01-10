import re
from GroupNode import GroupNode
from PythonNode import PythonNode
from TextNode import TextNode

TOKENS = {
    '{{' : 'startvar',
    '}}' : 'endvar',
    '{%' : 'starttag',
    '%}' : 'endtag',
    }

class ParseException(Exception):
    pass


class Parser:
    def __init__(self, text):
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

    def next(self):
        if not self.end():
            self._upto += 1

    def expand(self, context={}):
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
            
            if keyword == 'include':
                child = self.parse_include()
            if self.peek() != 'endtag':
                raise ParseError('No end tag')
            self.next()
        else:
            child = self.parse_text()

        
        group = self.parse_group()
        group.children = [child] + group.children

        return group

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


text = 'This is some text {{1 + 2 + 3}} var + 1 = {{var + 1}} empty = {{}} {% include template.html %}'
p = Parser(text)
print(p.expand({'var' : 6}))
