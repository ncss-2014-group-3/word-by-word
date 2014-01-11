from template_engine import parser

p = parser.Parser("var is {{ var }}")
text = p.expand({"var": "hello"})
print(text)
