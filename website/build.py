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

    print(jobs)

    for j in jobs:
        j.run()


# env_jinja2 = jinja2.Environment(loader=jinja2.FileSystemLoader("templates"))


# def discover(path):
#     logging.info("Started discovery in \"{}\"".format(path))
#     all_dirs, all_files = website.util.list_all(path)
#     md_files, other_files = website.util.filter_ext(all_files, ".md")

#     md_updates = []
#     for md in md_files:
#         p = os.path.join(website.config.build_dir, md)
#         dst = website.util.change_ext(p, ".html")
#         if website.util.file_needs_update(md, dst):
#             logging.info("Page {} needs update".format(dst))
#             md_updates.append((md, dst))
#         else:
#             logging.info("Page {} is up to date".format(dst))

#     other_updates = []
#     for f in other_files:
#         dst = os.path.join(website.config.build_dir, f)
#         if website.util.file_needs_update(f, dst):
#             logging.info("File {} needs update".format(dst))
#             other_updates.append((f, dst))
#         else:
#             logging.info("File {} is up to date".format(dst))

#     return (all_dirs, md_updates, other_updates)


# def create_dirs(dirs):
#     for d in dirs:
#         p = os.path.join(website.config.build_dir, d)
#         if not os.path.exists(p):
#             logging.info("Create directory \"{}\"".format(p))
#             os.mkdir(p)
#         else:
#             logging.info("Skip existing directory \"{}\"".format(p))


# def render_pages(updates):
#     for u in updates:
#         logging.info("Render page {} -> {}".format(u[0], u[1]))
#         with open(u[0]) as i:
#             with open(u[1], "w") as o:
#                 md = i.read()
#                 var, md = website.markdown.extract_meta_data(md)
#                 if var is None:
#                     var = {}
#                 var["page_dirs"] = website.config.search_paths
#                 var["content"] = website.markdown.markdown(md)
#                 o.write(env_jinja2.get_template("page.html").render(var))


# def copy_files(updates):
#     for u in updates:
#         logging.info("Copy file {} -> {}".format(u[0], u[1]))
#         shutil.copy2(u[0], u[1])


# def create_css():
#     css = ""
#     for c in website.config.css_files:
#         with open(os.path.join("css", c)) as f:
#             css += f.read()
#     with open(os.path.join(website.config.build_dir, "page.css"), "w") as f:
#         f.write(css)


# def update():
#     logging.info("Start update")
#     if not os.path.exists(website.config.build_dir):
#         os.mkdir(website.config.build_dir)

#     for d in website.config.search_paths:
#         p = os.path.join(website.config.build_dir, d)
#         if not os.path.exists(p):
#             os.mkdir(p)

#         dirs, mds, files = discover(d)

#         create_dirs(dirs)
#         render_pages(mds)
#         copy_files(files)

#     extra_pages = []
#     extra_updates = []
#     for f in website.config.extra_files:
#         dst = os.path.join(website.config.build_dir, f)
#         _, ext = os.path.splitext(f)
#         if ext == ".md":
#             dst = website.util.change_ext(dst, ".html")
#             if website.util.file_needs_update(f, dst):
#                 extra_pages.append((f, dst))
#         else:
#             if website.util.file_needs_update(f, dst):
#                 extra_updates.append((f, dst))
#     render_pages(extra_pages)
#     copy_files(extra_updates)

#     create_css()

#     logging.info("Done!")
