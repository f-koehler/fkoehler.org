import toucan.job.basic
import toucan.markdown
import toucan.config


class MarkdownJob(toucan.job.basic.FileJob):
    def run(self):
        with open(self.sources[0]) as f:
            md = f.read()
        _, md = toucan.markdown.extract_meta_data(md)
        html = toucan.markdown.markdown.render(md)
        with open(self.destination, "w") as f:
            f.write(html)

    @staticmethod
    def create(files):
        jobs = []
        for f in files:
            p = os.path.join(toucan.config.build_dir, f)
            j = MarkdownJob(f)
            jobs += j.required_jobs()
            jobs.append(j)
        return jobs
