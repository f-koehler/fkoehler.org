import os.path


class Job:
    def __init__(self, destination):
        self.destination = os.path.normpath(os.path.abspath(destination))

    def __eq__(self, other):
        if isinstance(other, Job):
            return self.destination == other.destination
        return NotImplemented

    def __ne__(self, other):
        result = self.__eq__(other)
        if result == NotImplemented:
            return NotImplemented
        return not result

    def __lt__(self, other):
        if isinstance(other, Job):
            return self.destination < other.destination
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, Job):
            return self.destination <= other.destination
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, Job):
            return self.destination >= other.destination
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, Job):
            return self.destination > other.destination
        return NotImplemented

    def required_jobs(self):
        pass

    def up_to_date(self):
        return True

    def run(self):
        pass


class JobTree:
    def __init__(self, job, parent=None):
        self.job = job
        self.left = None
        self.right = None
        self.parent = parent

    def insert(self, job):
        if self.job == job:
            return
        if self.left is None:
            self.left = JobTree(job, self)
            return
        if job <= self.job:
            self.left.insert(job)
            return
        if self.right is None:
            self.right = JobTree(job, self)
            return
        self.right.insert(job)

    def run(self):
        if not self.job.up_to_date():
            self.job.run()
        if self.left is not None:
            self.left.run()
        if self.right is not None:
            self.right.run()
