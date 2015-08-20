import mistune
import pygments
import pygments.formatters
import pygments.lexers


class Renderer(mistune.Renderer):
    def block_code(self, code, lang):
        if not lang:
            return "\n<pre><code>{}</pre></code>".format(mistune.excape(code))
        lexer = pygments.lexers.get_lexer_by_name(lang)
        formatter = pygments.formatters.HtmlFormatter()
        return pygments.highlight(code, lexer, formatter)

renderer = Renderer()
markdown = mistune.Markdown(renderer=renderer)
