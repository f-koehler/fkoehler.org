import os
import os.path

import website.config
import website.job


def extra_jobs():
    jobs = []
    for f in website.config.extra_files:
        base, ext = os.path.splitext(f)
        if ext == ".md":
            src = f
            dst = os.path.join(website.config.build_dir, base+".html")
            j = website.job.PageJob(src, dst, "page.html")
            req = j.generate_required_jobs()
            jobs += req+[j]
    return jobs


def page_jobs(path):
    jobs = []
    items = []
    index_page = os.path.join(path, "index.md")
    for root, _, files in os.walk(path):
        for f in files:
            src = os.path.join(root, f)
            if src == index_page:
                continue
            base, ext = os.path.splitext(src)
            if ext == ".md":
                dst = os.path.join(website.config.build_dir, base + ".html")
                j = website.job.PageJob(src, dst, "page.html")
                if j.meta:
                    title = "undefined"
                    if "title" in j.meta:
                        title = j.meta["title"]
                    date = "undefined"
                    if "date" in j.meta:
                        date = j.meta["date"]
                    brief = "undefined"
                    if "brief" in j.meta:
                        brief = j.meta["brief"]
                    items.append(("todo", title, date, brief))
                jobs += j.generate_required_jobs()
                jobs.append(j)
    base, ext = os.path.splitext(index_page)
    j = website.job.PageJob(index_page, os.path.join(website.config.build_dir, base+".html"), "pagelist.html")
    j.meta["pages"] = items
    return jobs+[j]


def css_job():
    j = website.job.CssJob(
        [os.path.join("css", f) for f in website.config.css_files],
        os.path.join(website.config.build_dir, "page.css")
    )
    return j.generate_required_jobs()+[j]


def run():
    jobs = css_job()
    jobs += extra_jobs()
    for p in website.config.search_paths:
        jobs += page_jobs(p)

    for j in jobs:
        j.run()
