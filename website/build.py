import os
import os.path

import website.config
import website.job
import website.markdown


def extra_jobs():
    jobs = []
    for f in website.config.extra_files:
        base, ext = os.path.splitext(f)
        if ext == ".md":
            src = f
            dst = os.path.join(website.config.build_dir, base+".html")
            j = website.markdown.PageJob(src, dst)
            req = j.generate_required_jobs()
            jobs += req+[j]
    return jobs


def page_jobs(path):
    jobs = []
    for root, _, files in os.walk(path):
        for f in files:
            base, ext = os.path.splitext(f)
            if ext == ".md":
                src = os.path.join(root, f)
                dst = os.path.join(website.config.build_dir, root, base+".html")
                j = website.markdown.PageJob(src, dst)
                req = j.generate_required_jobs()
                jobs += req+[j]
    return jobs


def css_job():
    css_files = [f for f in os.listdir("css") if os.path.isfile(os.path.join("css", f))]
    return [website.job.CssJob(css_files, os.path.join(website.config.build_dir, "page.css"))]


def run():
    jobs = css_job()
    jobs += extra_jobs()
    for p in website.config.search_paths:
        jobs += page_jobs(p)

    for j in jobs:
        j.run()
