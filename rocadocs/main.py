import json
import os
import errno
import markdown
import codecs
import re
import argparse
from rocadocs.extension import RocaExtension
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


def autoindex(files, root, directory):
    buf = '<ul class="autoindex">'
    for file in files:
        full_file = os.path.join(directory, file)
        relative_to_root = full_file.replace(root, '').lstrip('/')
        is_dir = os.path.isdir(full_file)
        sub = ''
        if is_dir:
            if file == '.git':
                continue
            relative_to_root += '-index'
            title = os.path.basename(file)
            subfiles = os.listdir(full_file)
            subfiles.sort(key=lambda f: -1 * int(os.path.isdir(os.path.join(directory, f))))
            sub = autoindex(subfiles, root, full_file)
        else:
            if not file.endswith('.md'):
                continue
            relative_to_root = relative_to_root[:-3]
            title = os.path.basename(file)[:-3]

        buf += '<li><span class="icon {3}"></span> <a href="javascript:article(\'{0}\')">{1}</a>{2}</li>\n'.format(
            slugify(relative_to_root),
            title_string(title),
            sub,
            'folder' if is_dir else 'file'
        )
    return buf + '</ul>'


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

        index_files = [
            os.path.join(directory, 'index.md'),
            os.path.join(directory, 'README.md'),
            os.path.join(directory, 'readme.md')
        ]

        index_file = os.path.join(directory, 'index.md')

        for index_file_test in index_files:
            if os.path.exists(index_file_test):
                index_file = index_file_test

        index_slug = slugify(os.path.relpath(index_file, root)[:-3])
        struct['id'] = index_slug

        files = os.listdir(directory)
        files.sort(key=lambda f: -1 * int(os.path.isdir(os.path.join(directory, f))))

        if os.path.exists(index_file) and os.path.isfile(index_file):
            struct['html'] = file_to_html(index_file)
        else:
            struct['html'] = autoindex(files, root, directory)
            struct['autoindex'] = True

        for filename in files:
            if filename == 'index.md' or filename == '.git' or filename == 'README.md' or filename == 'readme.md':
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

    print('Done: {0}'.format(target_file))
