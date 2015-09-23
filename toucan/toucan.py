import os
import os.path

import toucan.config
import toucan.jobtree
import toucan.job.basic


def generate_jobs(path):
    files = dict()
    for root, _, f in os.walk(path):
        path = os.path.splitext(root, f)
        _, ext = os.path.splitext(path)
        if ext not in files:
            files[ext] = [path]
        else:
            files[ext].append(path)

    jobs = []
    for ext, fs in files:
        jobs += toucan.config.job_map[ext](files[ext])

    return jobs


def create_tree():
    j = toucan.job.basic.DirJob(toucan.config.build_dir)
    tree = toucan.jobtree.JobTree(j)
    for p in toucan.config.search_paths:
        jobs = generate_jobs(p)
        for j in jobs:
            tree.insert(j)
    return tree

# import logging
# import os
# import os.path

# import website.config
# import website.job


# def log_add_job(job):
#     logging.info("Add: {}".format(job))


# def log_add_jobs(jobs):
#     for j in jobs:
#         logging.info("Add: {}".format(j))


# def log_run_job(job):
#     logging.info("Run: {}".format(job))


# def extra_jobs():
#     jobs = []
#     for f in website.config.extra_files:
#         base, ext = os.path.splitext(f)
#         if ext == ".md":
#             src = f
#             dst = os.path.join(website.config.build_dir, base+".html")
#             j = website.job.PageJob(src, dst, "page.html")
#             log_add_job(j)
#             req = j.generate_required_jobs()
#             log_add_jobs(req)
#             jobs += req+[j]
#     return jobs


# def page_jobs(path):
#     jobs = []
#     items = []
#     index_page = os.path.join(path, "index.md")
#     for root, _, files in os.walk(path):
#         for f in files:
#             src = os.path.join(root, f)
#             if src == index_page:
#                 continue
#             base, ext = os.path.splitext(src)
#             if ext == ".md":
#                 dst = os.path.join(website.config.build_dir, base + ".html")
#                 j = website.job.PageJob(src, dst, "page.html")
#                 if j.meta:
#                     title = "undefined"
#                     if "title" in j.meta:
#                         title = j.meta["title"]
#                     date = "undefined"
#                     if "date" in j.meta:
#                         date = j.meta["date"]
#                     brief = "undefined"
#                     if "abstract" in j.meta:
#                         brief = j.meta["abstract"]
#                     items.append(("/"+base+".html", title, date, brief))
#                 log_add_job(j)
#                 req = j.generate_required_jobs()
#                 log_add_jobs(req)
#                 jobs += req+[j]
#     base, ext = os.path.splitext(index_page)
#     j = website.job.PageJob(index_page, os.path.join(website.config.build_dir, base+".html"), "pagelist.html")
#     j.meta["pages"] = items
#     return jobs+[j]


# def css_job():
#     j = website.job.CssJob(
#         [os.path.join("css", f) for f in website.config.css_files],
#         os.path.join(website.config.build_dir, "page.css")
#     )
#     log_add_job(j)
#     return j.generate_required_jobs()+[j]


# def run():
#     jobs = css_job()
#     jobs += extra_jobs()
#     for p in website.config.search_paths:
#         jobs += page_jobs(p)

#     for j in jobs:
#         log_run_job(j)
#         j.run()
