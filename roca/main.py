import fnmatch
import os
import errno
import markdown
from shutil import copytree, rmtree
from markdown.extensions.nl2br import Nl2BrExtension
from roca.extension import RocaExtension
from jinja2 import Environment, FileSystemLoader
from natsort import natsorted, ns


def mkdir_nested(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def find_files(directory):
    r = []
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, '*.md'):
                filename = os.path.join(root, basename)
                r.append(filename)
    return r


def main():
    env = Environment(loader=FileSystemLoader('./themes/default/'))
    page = env.get_template('page.html')

    md = markdown.Markdown(extensions=[
        Nl2BrExtension(),
        RocaExtension()
    ])

    root = os.path.abspath('./docs/')
    target = os.path.abspath('./target/')

    if os.path.exists(target) and os.path.isdir(target):
        rmtree(target, True)

    assets_target = os.path.join(target, 'assets')
    copytree('./themes/default/assets/', assets_target)

    mkdir_nested(target)

    source_files = find_files(root)

    buf = ''
    for filename in source_files:
        with open(filename, 'r') as source_file:
            buf += '\n\n' + source_file.read()
            source_file.close()

    contents = md.convert(buf)

    with open('target/index.html', 'w') as target_file:
        html = page.render(
            body=contents
        )
        target_file.truncate()
        target_file.write(html)
        target_file.close()
