import mistune
import re
import pygments
import pygments.formatters
import pygments.lexers

import website.job


regex_meta_block = re.compile(r"---+\n(?P<data>(?:.*\n)*)---+", re.MULTILINE)
regex_meta_line = re.compile(r"(?P<key>[^\:]+)\s*\:\s*(?P<value>.+)")


class InlineGrammar(mistune.InlineGrammar):
    math = re.compile(r"^\$\$(.+?)\$\$", re.DOTALL)
    block_math = re.compile(r"^\\\[(.+?)\\\]", re.DOTALL)


class BlockGrammar(mistune.BlockGrammar):
    block_math = re.compile(r"^\\\[(.+?)\\\]", re.DOTALL)


class InlineLexer(mistune.InlineLexer):
    default_rules = ["block_math", "math"] + mistune.InlineLexer.default_rules

    def __init__(self, renderer, **kwargs):
        rules = InlineGrammar()
        super(InlineLexer, self).__init__(renderer, rules, **kwargs)

    def output_math(self, m):
        return self.renderer.inline_math(m.group(1))

    def output_block_math(self, m):
        return self.renderer.block_math(m.group(1))


class BlockLexer(mistune.BlockLexer):
    default_rules = ["block_math"] + mistune.BlockLexer.default_rules

    def __init__(self, **kwargs):
        rules = BlockGrammar()
        super(BlockLexer, self).__init__(rules, **kwargs)

    def parse_block_math(self, m):
        self.tokens.append({
            "type": "block_math",
            "text": m.group(1)
        })


class Renderer(mistune.Renderer):
    def block_math(self, math):
        return "\\[%s\\]" % math

    def inline_math(self, math):
        return "@@%s@@" % math


class Markdown(mistune.Markdown):
    def __init__(self, **kwargs):
        kwargs["inline"] = InlineLexer
        kwargs["block"] = BlockLexer
        super(Markdown, self).__init__(Renderer(), **kwargs)

    def output_block_math(self):
        return self.renderer.block_math(self.token["text"])


def extract_meta_data(markdown):
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


renderer = Renderer()
inline = InlineLexer(renderer)
block = BlockLexer()
markdown = mistune.Markdown(renderer=renderer, inline=inline, block=block)
