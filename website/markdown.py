import mistune
import pygments
import pygments.formatters
import pygments.lexers
import re

import website.job


regex_meta_block = re.compile(r"---+\n(?P<data>(?:.*\n)*)---+", re.MULTILINE)
regex_meta_line = re.compile(r"(?P<key>[^\:]+)\s*\:\s*(?P<value>.+)")


class Renderer(mistune.Renderer):
    def block_code(self, code, lang):
        if not lang:
            return "\n<pre><code>{}</pre></code>".format(mistune.excape(code))
        lexer = pygments.lexers.get_lexer_by_name(lang)
        formatter = pygments.formatters.HtmlFormatter()
        return pygments.highlight(code, lexer, formatter)

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


def pygments_css(style):
    formatter = pygments.formatters.HtmlFormatter(style=style)
    return formatter.get_style_defs(".highlight")


renderer = Renderer()
markdown = mistune.Markdown(renderer=renderer)
