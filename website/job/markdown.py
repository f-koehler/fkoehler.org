import website.job.basic
import website.markdown


class MarkdownJob(website.job.basic.FileJob):
    def run(self):
        with open(self.sources[0]) as f:
            md = f.read()
        _, md = website.markdown.extract_meta_data(md)
        html = website.markdown.markdown.render(md)
        with open(self.destination, "w") as f:
            f.write(html)
