import website.job.basic


class CssJob(website.job.basic.FileJob):
    def run(self):
        css = ""
        for src in self.sources:
            with open(src) as f:
                css.append(f.read(src))
        with open(self.destination) as f:
            f.write(css)

    @staticmethod
    def create(files):
        j = CssJob(files)
        return j.required_jobs()+[j]
