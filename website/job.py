import os
import os.path
import shutil
import jinja2

import website.markdown


template_env = jinja2.Environment(loader=jinja2.FileSystemLoader("templates"))


def file_up_to_date(self, src, dst):
    return os.path.getmtime(src) > os.path.getmtime(dst)


class Job(object):
    def up_to_date(self):
        pass

    def generate_required_jobs(self):
        return []

    def run(self):
        pass


class DirCreationJob(Job):
    directory = ""

    def __init__(self, directory):
        self.directory = directory

    def __repr__(self):
        return "mkdir: {}".format(self.directory)

    def up_to_date(self):
        if not os.path.exists(self.directory):
            return False
        return True

    def run(self):
        if self.up_to_date():
            return
        os.makedirs(self.directory)


class FileJob(Job):
    src = ""
    dst = ""

    def __init__(self, src, dst):
        self.src = src
        self.dst = dst

    def __repr__(self):
        return "file: {} => {}".format(self.src, self.dst)

    def up_to_date(self):
        if not os.path.exists(self.dst):
            return False

        if isinstance(self.src, str):
            if not os.path.exists(self.src):
                # TODO: raise exception
                return
            return self.file_up_to_date(self.src, self.dst)
        elif isinstance(self.src, list):
            for s in self.src:
                if not os.path.exists(s):
                    # TODO: raise exception
                    return
                if self.file_up_to_date(s, self.dst):
                    return False
            return True
        else:
            # TODO: raise exception
            return

    def generate_required_jobs(self):
        job = DirCreationJob(os.path.dirname(self.dst))
        return job.generate_required_jobs()+[job]

    def run(self):
        pass


class FileCopyJob(FileJob):
    def __repr__(self):
        return "cp: {} => {}".format(self.src, self.dst)

    def run(self):
        if self.up_to_date():
            return
        shutil.copy2(self.src, self.dst)


class CssJob(FileJob):
    def __repr__(self):
        return "css: {} => {}".format(self.src, self.dst)

    def run(self):
        if self.up_to_date():
            return
        if not isinstance(self.src, list):
            # TODO: raise exception
            return
        css = ""
        for s in self.src:
            with open(s) as f:
                css += f.read()
        with open(self.dst, "w") as f:
            f.write(css)


class PageJob(Job):
    def __init__(self, src, dst, template_name="page.html"):
        self.src = src
        self.dst = dst
        self.template_name = template_name
        with open(self.src) as f:
            self.meta, self.md = website.markdown.renderer.extract_meta_data(f.read())
        if not self.meta:
            self.meta = dict()

    def __repr__(self):
        path = os.path.join("templates", self.template_name)
        return "md:  {} + {} => {}".format(self.src, path, self.dst)

    def up_to_date(self):
        if not os.path.exists(self.dst):
            return False

        if not file_up_to_date(self.src, self.dst):
            return False

        path = os.path.join("templates", self.template_name)
        if not file_up_to_date(path, self.dst):
            return False

        return True

    def generate_required_jobs(self):
        return [DirCreationJob(os.path.dirname(self.dst))]

    def run(self):
        var = self.meta
        if not var:
            var = dict()
        var["content"] = website.markdown.markdown(self.md)
        var["menu_items"] = website.config.menu_items
        with open(self.dst, "w") as f:
            f.write(template_env.get_template(self.template_name).render(var))
