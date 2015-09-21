import os
import os.path
import website.jobtree


class FileJob(website.jobtree.Job):
    def __init__(self, destination, sources=[]):
        self.destination = destination
        self.sources = sources

    def up_to_date(self):
        if not os.path.exists(self.destination):
            return False
        dst_time = os.path.getmtime(self.destination)
        for src in self.sources:
            # TODO: fail if source does not exists
            src_time = os.path.getmtime(src)
            if src_time > dst_time:
                return False
        return True

    def run(self):
        pass

    def required_jobs(self):
        jobs = []
        d = os.path.dirname(self.destination)
        jobs.append(DirJob(d))
        return jobs


class DirJob(website.jobtree.Job):
    def up_to_date(self):
        if os.path.exists(self.destination):
            return False
        return True

    def run(self):
        os.makedirs(self.destination)
