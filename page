#!/usr/bin/python
import http.server
import logging
import os
import os.path
import shutil
import sys
import website.build
import website.markdown
import website.config


def usage():
    msg = (
        "usage: ./run.py <command>\n\n"
        "commands:\n"
        "  help\t\tprint this message\n"
        "  build\t\tbuilds the site\n"
        "  preview\tpreview the site on port {}\n"
        "  clean\t\tdeletes the build dir \"{}\"\n"
        "  codecss\twrites the code css file for a certain style\n"
    ).format(website.config.preview_port, website.config.build_dir)
    print(msg, file=sys.stderr)


def preview():
    os.chdir(website.config.build_dir)
    address = ('', 8888)
    handler = http.server.SimpleHTTPRequestHandler
    server = http.server.HTTPServer(address, handler)
    server.serve_forever()

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("Error: No command specified!", file=sys.stderr)
        usage()
        exit(1)

    cmd = sys.argv[1]
    if cmd not in ["help", "build", "preview", "clean", "codecss"]:
        print("Error: Unknown command \""+cmd+"\"!", file=sys.stderr)
        usage()
        exit(1)

    if cmd == "help":
        usage()
        exit(1)

    logging.basicConfig(level=logging.INFO)

    if cmd == "build":
        website.build.run()
        exit(0)

    if cmd == "preview":
        preview()
        exit(0)

    if cmd == "clean":
        if os.path.exists(website.config.build_dir):
            shutil.rmtree(website.config.build_dir)
        exit(0)

    if cmd == "codecss":
        if len(sys.argv) <= 2:
            print("Error: Specify a style!", file=sys.stderr)
            exit(1)
        with open(os.path.join("css", "code.css"), "w") as f:
            f.write(website.markdown.pygments_css(sys.argv[2]))
        exit(0)
