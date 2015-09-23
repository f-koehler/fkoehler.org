import os.path

import toucan.job.basic
import toucan.config


class CssJob(toucan.job.basic.FileJob):
    def run(self):
        css = ""
        for src in self.sources:
            with open(src) as f:
                css.append(f.read(src))
        with open(self.destination) as f:
            f.write(css)

    @staticmethod
    def create(files):
        p = os.path.join(toucan.config.build_dir, "page.css")
        j = CssJob(p, files)
        return j.required_jobs()+[j]
