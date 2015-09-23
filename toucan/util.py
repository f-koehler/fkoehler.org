import datetime
import dateutil.tz
import os
import os.path


# TODO: create css only if one file updated
# TODO: rebuild pages if template changed


def now():
    """
    Return the current time (in the local time zone).

    :returns: The current time.
    :rtype: datetime
    """
    return datetime.datetime.now(dateutil.tz.tzlocal())


def time_rfc822(dt=now()):
    """
    Format a datetime object to a RFC 822 compatible string

    :param datetime dt: The datetime object to format.
    :returns: A RFC 822 compatible string
    :rtype: str
    """
    return dt.strftime("%d %b %Y %H:%M %z")


def file_needs_update(src, dst):
    if not os.path.exists(dst):
        return True
    return os.path.getmtime(src) > os.path.getmtime(dst)


def list_all(path):
    ds = []
    fs = []
    for root, dirs, files in os.walk(path):
        for d in dirs:
            ds.append(os.path.join(root, d))
        for f in files:
            fs.append(os.path.join(root, f))
    return (ds, fs)


def filter_ext(files, ext):
    matches = []
    remainders = []
    for f in files:
        _, e = os.path.splitext(f)
        if e == ext:
            matches.append(f)
        else:
            remainders.append(f)
    return (matches, remainders)


def change_ext(path, ext):
    root, _ = os.path.splitext(path)
    return root+ext
