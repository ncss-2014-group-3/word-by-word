import re
from GroupNode import GroupNode
from PythonNode import PythonNode
from TextNode import TextNode

TOKENS = re.compile(r'{{|}}|(?:[^{}]|{[^{]|}[^}])*', re.DOTALL)

class ParseException(Exception):
    pass


class Parser:
    def __init__(self, text):
        self._tokens = TOKENS.findall(text)
        self._length = len(self._tokens)
        self._upto = 0

    def end(self):
        return self._upto == self._length

    def peek(self):
        return None if self.end() else self._tokens[self._upto]

    def next(self):
        if not self.end():
            self._upto += 1


    def parse_group(self):
        children = []
        while not self.end():
            if self.peek() == '{{':
                self.next()
                children.append(self.parse_python())
                if self.peek() != '}}':
                    raise ParseException('No closing "}}"')
                self.next()
            else:
                children.append(self.parse_text())
        return GroupNode(children)

    def parse_python(self):
        if self.peek() == '}}':
            return PythonNode('')
        result = PythonNode(self.peek())
        self.next()
        return result

    def parse_text(self):
        result = TextNode(self.peek())
        self.next()
        return result
