# build_dir = "build"
# css_files = ["normalize.css", "code.css", "links.css", "nav.css", "page.css"]
# extra_files = ["index.md", "404.md"]
# preview_port = 8888
# search_paths = ["computer", "physics"]

# menu_items = [
#     ("/", "Home"),
#     ("/computer", "Computer"),
#     ("/physics", "Physics"),
# ]
from toucan.job.css import CssJob
from toucan.job.markdown import MarkdownJob
from toucan.job.tikz import TikzJob

build_dir = "build"

job_map = {
    ".css": CssJob.create,
    ".md": MarkdownJob.create,
    ".tikz": TikzJob.create
}

search_paths = [
    "computer",
    "physics"
]

extra_files = [
    "index.md",
    "404.md"
]
