import os.path
import hashlib
import subprocess
import shutil
import website.job.basic


backend = "lualatex"


class TikzJob(website.job.basic.FileJob):
    def run(self):
        source = self.sources[0]
        if not os.path.exists(source):
            # TODO: fail
            pass
        sha = hashlib.sha256(self.destination).hexdigest()
        tmpdir = os.path.join("/tmp", sha)
        os.mkdir(tmpdir)
        subprocess.check_output([
            backend,
            "--interaction=errorstopmode",
            "--output-directory="+tmpdir,
            source,
        ])
        pdffile = os.path.join(tmpdir, os.path.basename(source))
        subprocess.check_output([
            "pdf2svg",
            pdffile,
            self.destination
        ])
        shutil.rmtree(tmpdir)

    @staticmethod
    def create(files):
        jobs = []
        for f in files:
            j = TikzJob(f)
            jobs += j.required_jobs()
            jobs.append(j)
        return jobs
