#!/usr/bin/python
import sys
import logging
import os.path
import shutil
import website.config
import website.build


def usage():
    msg = (
        "usage: ./run.py <command>\n\n"
        "commands:\n"
        "  help\t\tprint this message\n"
        "  build\t\tbuilds the site\n"
        "  preview\tpreview the site on port {}\n"
        "  clean\t\tdeletes the build dir \"{}\"\n"
    ).format(website.config.preview_port, website.config.build_dir)
    print(msg, file=sys.stderr)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Error: No command specified!", file=sys.stderr)
        usage()
        exit(1)

    cmd = sys.argv[1]
    if cmd not in ["help", "build", "preview", "clean"]:
        print("Error: Unknown command \""+cmd+"\"!", file=sys.stderr)
        usage()
        exit(1)

    if cmd == "help":
        usage()
        exit(1)

    logging.basicConfig(level=logging.INFO)

    if cmd == "build":
        website.build.update()
        exit(0)

    if cmd == "preview":
        exit(0)

    if cmd == "clean":
        if os.path.exists(website.config.build_dir):
            shutil.rmtree(website.config.build_dir)
        exit(0)
