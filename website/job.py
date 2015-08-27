import os
import os.path
import shutil


class Job(object):
    """
    Base class for all jobs
    """

    def up_to_date(self):
        """
        This method checks whether the job is up-to-date or not.

        :returns: True if job is up-to-date.
        :rtype: bool
        """
        pass

    """
    Return a list of jobs required by this job.

    :rtype: list
    """
    def generate_required_jobs(self):
        return []

    """
    Run the job.
    """
    def run(self):
        pass


class DirCreationJob(Job):
    """
    Job class for directory creation
    """

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
    """
    Job class for file operations
    """

    src = ""
    dst = ""

    def __init__(self, src, dst):
        self.src = src
        self.dst = dst

    def __repr__(self):
        return "file: {} => {}".format(self.src, self.dst)

    def file_up_to_date(self, src, dst):
        return os.path.getmtime(src) > os.path.getmtime(dst)

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
    """
    Job to copy file
    """
    def __repr__(self):
        return "cp: {} => {}".format(self.src, self.dst)

    def run(self):
        if self.up_to_date():
            return
        shutil.copy2(self.src, self.dst)


class CssJob(FileJob):
    """
    Job to concatenate css files into one file
    """
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
