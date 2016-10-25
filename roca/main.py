import json
import os
import errno
import markdown
import codecs
import re
import argparse
from roca.extension import RocaExtension
from slugify import slugify

md = markdown.Markdown(extensions=[
    RocaExtension()
])


def mkdir_nested(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def file_to_html(path):
    with codecs.open(path, 'r', 'utf-8') as md_file:
        html = md.convert(md_file.read().lstrip('\ufeff'))
        md_file.close()
        return html


def title_string(text):
    t = text.replace('-', ' ').replace('_', ' ')
    return re.sub(r'((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))', r' \1', t)


def main():
    parser = argparse.ArgumentParser(description='Generate data.json used by Roca-Web')
    parser.add_argument('--source', help='Source directory of the Markdown files', type=str, required=True)
    parser.add_argument('--target', help='Target directory to generate data.json in', default='.', type=str)
    parser.add_argument('--title', help='Project title', default='Documentation', type=str)

    args = parser.parse_args()

    root = os.path.abspath(args.source)
    target = os.path.abspath(args.target)

    if not os.path.isdir(target):
        mkdir_nested(target)

    def scan(directory):
        struct = {
            'name': title_string(os.path.basename(directory)),
            'html': '',
            'children': []
        }

        index_file = os.path.join(directory, 'index.md')
        if os.path.exists(index_file) and os.path.isfile(index_file):
            struct['html'] = file_to_html(index_file)
            struct['id'] = slugify(os.path.relpath(index_file, root)[:-3])

        for filename in os.listdir(directory):
            if filename == 'index.md':
                continue
            full_path = os.path.join(directory, filename)
            if os.path.isdir(full_path):
                struct['children'].append(scan(full_path))
            elif filename.endswith('.md'):
                struct['children'].append({
                    'name': title_string(os.path.basename(filename)[:-3]),
                    'html': file_to_html(full_path),
                    'id': slugify(os.path.relpath(full_path, root)[:-3])
                })

        return struct

    struct = scan(root)

    struct['name'] = args.title

    data = {
        'title': args.title,
        'tree': struct
    }

    target_file = os.path.join(target, 'data.json')

    json.dump(data, open(target_file, 'w'))
