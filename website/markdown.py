import mistune
import re
import pygments
import pygments.formatters
import pygments.lexers

import website.job


regex_meta_block = re.compile(r"---+\n(?P<data>(?:.*\n)*)---+", re.MULTILINE)
regex_meta_line = re.compile(r"(?P<key>[^\:]+)\s*\:\s*(?P<value>.+)")


class InlineLexer(mistune.InlineLexer):
    pass


class BlockLexer(mistune.BlockLexer):
    pass


class CodeRendererMixin(object):
    def block_code(self, code, lang):
        if not lang:
            code = code.strip()
            return "\n<pre><code>{}</pre></code>".format(mistune.escape(code))

        linenos = self.options.get("linenos")

        try:
            lexer = pygments.lexers.get_lexer_by_name(lang, stripall=True)
            formatter = pygments.formatters.HtmlFormatter(linenos=linenos)
            return pygments.highlight(code, lexer, formatter)
        except:
            code = code.strip()
            return "\n<pre><code>{}</pre></code>".format(mistune.excape(code))


class Renderer(CodeRendererMixin, mistune.Renderer):
    def extract_meta_data(self, markdown):
        m = regex_meta_block.match(markdown)
        if not m:
            return (None, markdown)
        data = m.groupdict()["data"].splitlines()
        markdown = markdown[len(m.group(0)):]

        meta = {}
        for l in data:
            m = regex_meta_line.match(l)
            if not m:
                # TODO: raise exception
                continue
            meta[m.groupdict()["key"]] = m.groupdict()["value"]
            meta["menu_items"] = website.config.menu_items
        return (meta, markdown)


# def pygments_css(style):
#     formatter = pygments.formatters.HtmlFormatter(style=style)
#     return formatter.get_style_defs(".highlight")


renderer = Renderer()
inline_lexer = InlineLexer(renderer)
block_lexer = BlockLexer(renderer)
markdown = mistune.Markdown(renderer, inline=inline_lexer)
