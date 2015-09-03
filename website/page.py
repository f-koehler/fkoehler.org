import os.path
import jinja2

import website.markdown


template_env = jinja2.Environment(loader=jinja2.FileSystemLoader("templates"))


class PageJob(website.job.FileJob):
    template_name = "page.html"
    extra_vars = dict()
    meta = None

    def __repr__(self):
        return "md: {} => {}".format(self.src, self.dst)

    def up_to_date(self):
        up2date = website.job.FileJob.up_to_date()
        path = os.path.join("templates", self.template_name)
        return up2date and website.util.file_needs_update(self.dst, path)

    def run(self):
        with open(self.src) as f:
            md = f.read()
            var, md = website.markdown.renderer.extract_meta_data(md)
            if not var:
                var = dict()
            else:
                self.meta = var
            var["content"] = website.markdown.markdown(md)
            var["page_dirs"] = website.config.menu_items
            var.update(self.extra_vars)
            with open(self.dst, "w") as f:
                f.write(template_env.get_template(self.template_name).render(var))
