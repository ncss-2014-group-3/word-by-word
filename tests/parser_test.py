import os
import sys

sys.path.insert(
    0,
    os.path.join(os.path.dirname(__file__), '..')
)

import unittest


from template_engine.parser import render_string, ParseException


class ParserTest(unittest.TestCase):
    def test_expressions(self):
        self.assertEqual(
            render_string('Test {{ 3 * 9 }}'),
            'Test 27'
        )

        self.assertEqual(
            render_string('Test {{ var + 3 }}', {'var': 9}),
            'Test 12'
        )

    def test_vars(self):
        context = {'var': "<p> <!-- --> \"\'\/ &amp; & #? <!CDATA[[ &"}

        self.assertEqual(
            render_string('Test {{ var }}', context),
            'Test &lt;p&gt; &lt;!-- --&gt; &quot;&#x27;'
            '\\/ &amp;amp; &amp; #? &lt;!CDATA[[ &amp;'
        )

    def test_var_resolution(self):
        template = 'var * 9 = {{ var * 9 }} WORDS! {{ 6 * 9 - (var + 4)}}'

        self.assertEqual(
            render_string(template, {'var': 1.4}),
            'var * 9 = 12.6 WORDS! 48.6'
        )

    def test_conditionals(self):
        text = 'Test words {% if var == 1 %} The world is good {% end if %} '

        self.assertEqual(
            render_string(text, {'var': 1}),
            'Test words  The world is good  '
        )

        self.assertEqual(
            render_string(text, {'var': 0}),
            'Test words  '
        )

    def test_advanced_conditionals(self):
        text = (
            '{% if var >= 1%}'
            '{%if var == 1 %}'
            'var = 1, '
            '{% end if %}'
            'var >= 1'
            '{% end if %}'
        )

        self.assertEqual(
            render_string(text, {'var': 1}),
            'var = 1, var >= 1'
        )

        self.assertEqual(
            render_string(text, {'var': 2}),
            'var >= 1'
        )

        self.assertEqual(
            render_string(text, {'var': 0}),
            ''
        )

        self.assertRaises(
            TypeError,
            render_string
            (text, {'var': ''})
        )

    def test_syntax_errors(self):
        self.assertRaises(
            ParseException,
            render_string,
            ('{% hello',)
        )

        self.assertRaises(
            ParseException,
            render_string,
            ('{% if 1 == 1 %}hello'),
        )

    def test_for_loops(self):
        template = (
            '{% for i in range(10) %}'
            '{{ i }} '
            '{% end for %}'
        )

        self.assertEqual(
            render_string(template, ),
            '0 1 2 3 4 5 6 7 8 9 '
        )

        template = (
            '{% for i in range(10) %}'
            '{% if i / 2 == int(i / 2) %}'
            '{{ i }} is divisible by two. '
            '{% end if %}'
            '{% end for %}'
        )

        self.assertEqual(
            render_string(template, ),
            '0 is divisible by two. '
            '2 is divisible by two. '
            '4 is divisible by two. '
            '6 is divisible by two. '
            '8 is divisible by two. '
        )

        self.assertRaises(
            ParseException,
            render_string,
            ('{% for i in range(5) %} {{ i }}',)
        )

        template = "{%for i in ('dog', 'cat', 'frog') %}{{ i }} {% end for %}"
        self.assertEqual(
            render_string(template, ),
            'dog cat frog '
        )

        template = (
            "{% for i in range(9) %}"
            '{% for j in "abcd"%}'
            '{{ str(i) + j }},'
            '{% end for %}'
            '{% end for %}'
        )

        self.assertEqual(
            render_string(template, ),
            '0a,0b,0c,0d,'
            '1a,1b,1c,1d,'
            '2a,2b,2c,2d,'
            '3a,3b,3c,3d,'
            '4a,4b,4c,4d,'
            '5a,5b,5c,5d,'
            '6a,6b,6c,6d,'
            '7a,7b,7c,7d,'
            '8a,8b,8c,8d,'
        )

    def test_else_clause(self):
        template = (
            '{% if var == 1 %}'
            'var = 1'
            '{% else %}'
            'var != 1'
            '{% end if %}'
        )

        self.assertEqual(
            render_string(template, {'var': 0}),
            'var != 1'
        )

        self.assertEqual(
            render_string(template, {'var': 1}),
            'var = 1'
        )

    def test_advanced_loops(self):
        template = (
            '{% for i,e in enumerate("abcde") %}'
            '{{e}} is the {{i}}th letter, '
            '{% end for%}'
        )

        self.assertEqual(
            render_string(template, ),
            'a is the 0th letter, '
            'b is the 1th letter, '
            'c is the 2th letter, '
            'd is the 3th letter, '
            'e is the 4th letter, '
        )

        text = (
            '{%for a in [i for i in range(10) if i == var] %} '
            '{{a}} == {{var}} '
            '{% else %}'
            'No numbers in 0..9 equal '
            '{{var}}'
            '{% end for %}'
        )
        self.assertEqual(
            render_string(text, {'var': 100}),
            'No numbers in 0..9 equal 100'
        )
        self.assertEqual(
            render_string(text, {'var': 5}),
            ' 5 == 5 '
        )

    def test_list_comprehension(self):
        self.assertEqual(
            render_string('{{[s for s in range(9) if s == var]}}', {'var': 5}),
            '[5]'
        )

    def test_json_directive(self):
        self.assertEqual(
            render_string('{%json {"bla":["a", "b"]}%}'),
            '{"bla": ["a", "b"]}'
        )


def main():
    unittest.main()

if __name__ == '__main__':
    main()
