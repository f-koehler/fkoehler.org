import os.path
import shutil
import jinja2
import website.util
import website.config
import website.markdown

env_jinja2 = jinja2.Environment(loader=jinja2.FileSystemLoader("templates"))

def discover(path):
    all_files, all_dirs = website.util.list_all(path)
    md_files, other_files = website.util.filter_ext(all_files)
    
    md_updates = []
    for md in md_files:
        dst = os.path.join(website.config.build_dir, md)
        if website.util.file_needs_update(md, dst):
            md_updates.append((md, website.util.change_ext(dst, ".html")))

    other_updates = []
    for f in other_files:
        dst = os.path.join(website.config.build_dir, f)
        if website.util.file_needs_update(f, dst):
            other_updates.append((f, dst))

    return (all_dirs, md_updates, other_updates)

def create_dirs(dirs):
    for d in dirs:
        p = os.path.join(website.config.build_dir, d)
        if not os.path.exists(p):
            os.mkdir(p)

def copy_files(updates):
    for u in updates:
        shutil.copy2(u[0], u[1])

def render_pages(updates):
    for u in updates:
        with open(u[0]) as i:
            with open(u[1], "w") as o:
                var = {}
                var["content"] = website.markdown.markdown(i.read())
                o.write(env_jinja2.get_template("page.html").render(var))

def update():
    if not os.path.exists(website.config.build_dir):
        os.mkdir(website.config.build_dir)

    for d in website.config.search_paths:
        dirs, mds, files = discover(d)

        create_dirs(dirs)
