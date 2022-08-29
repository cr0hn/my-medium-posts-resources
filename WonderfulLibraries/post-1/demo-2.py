from pygments.lexers.html import HtmlLexer
from prompt_toolkit.shortcuts import prompt
from prompt_toolkit.lexers import PygmentsLexer

text = prompt('Hi Medium! Enter HTML: ', lexer=PygmentsLexer(HtmlLexer))
print('You wrote: %s' % text)
