import re
import os.path

import jinja2
import mistune
import pygments
import pygments.formatters
import pygments.lexers

import website.job


template_env = jinja2.Environment(loader=jinja2.FileSystemLoader("templates"))
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
        return (meta, markdown)


def pygments_css(style):
    formatter = pygments.formatters.HtmlFormatter(style=style)
    return formatter.get_style_defs(".highlight")


renderer = Renderer()
markdown = mistune.Markdown(renderer=renderer)


class PageJob(website.job.FileJob):
    templates = ["page.html"]

    def __repr__(self):
        return "md: {} => {}".format(self.src, self.dst)

    def up_to_date(self):
        result = website.job.FileJob.up_to_date()
        for t in self.templates:
            path = os.path.join("templates", t)
            result = result and self.file_up_to_date(path, self.dst)
        return result

    def run(self):
        with open(self.src) as f:
            md = f.read()

        var, md = renderer.extract_meta_data(md)
        if not var:
            var = {}
        var["content"] = markdown(md)
        var["page_dirs"] = website.config.search_paths

        with open(self.dst, "w") as f:
            f.write(template_env.get_template("page.html").render(var))
