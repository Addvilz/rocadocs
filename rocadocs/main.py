import argparse
import codecs
import errno
import json
import os
import re

import markdown
from slugify import slugify

from rocadocs.const import *
from rocadocs.extension import RocaExtension

md = markdown.Markdown(extensions=[
    RocaExtension()
])

VERBOSE = False


class NotAFileError(Exception):
    pass


class NotADirectoryError(Exception):
    pass


class ExpectedDirectoryError(Exception):
    pass


def _print(message):
    if VERBOSE:
        print(message)


def is_blacklisted(path):
    base = os.path.basename(path).lower()
    if base in BLACKLISTED_DIRS or base in BLACKLISTED_FILES:
        return True
    return False


def mkdir_nested(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def file_to_html(file_path):
    if not os.path.isfile(file_path):
        raise NotAFileError(file_path)

    with codecs.open(file_path, 'r', 'utf-8') as srw:
        html = md.convert(srw.read().lstrip('\ufeff'))
        srw.close()
        return html


def title_string(text):
    t = text.replace('-', ' ').replace('_', ' ')
    return re.sub(r'((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))', r' \1', t)


def auto_index(directory, root):
    files = files_in_directory_sorted(directory)
    buf = '<ul class="autoindex">'
    for file in files:
        is_dir = os.path.isdir(file)
        sub = ''
        if is_dir:
            sub = auto_index(file, root)

        buf += '<li><span class="icon {3}"></span> <a href="javascript:article(\'{0}\')">{1}</a>{2}</li>\n'.format(
            path_to_slug(file, root),
            path_to_title(file),
            sub,
            'folder' if is_dir else 'file'
        )
    return buf + '</ul>'


def main():
    global VERBOSE
    VERBOSE = True
    parser = argparse.ArgumentParser(description='Generate data.json used by Roca-Web')
    parser.add_argument('--source', help='Source directory of the Markdown files', type=str, required=True)
    parser.add_argument('--target', help='Target directory to generate data.json in', default='.', type=str)
    parser.add_argument('--title', help='Project title', default='Documentation', type=str)

    args = parser.parse_args()

    root = os.path.abspath(args.source)

    target = os.path.abspath(args.target)

    build(root, target, args.title)


def files_in_directory_sorted(directory):
    files = os.listdir(directory)
    files.sort(key=lambda file: -1 * int(os.path.isdir(os.path.join(directory, file))))
    return [os.path.join(directory, file) for file in files if not is_blacklisted(file)]


def find_index_file_in_directory(directory):
    files = [f.lower() for f in os.listdir(directory)]

    for file in INDEX_FILES:
        for ext in VALID_EXTENSIONS:
            expected = file + ext
            if expected in files:
                return os.path.join(directory, expected)
    return None


def is_markdown_file(path):
    if not os.path.isfile(path):
        return False
    for ext in VALID_EXTENSIONS:
        if path.endswith(ext):
            return True
    return False


def remove_known_extension(path):
    lower_path = path.lower()
    for ext in VALID_EXTENSIONS:
        if lower_path.endswith(ext):
            return path[:-(len(ext))]
    return path


def path_to_title(path):
    base = remove_known_extension(os.path.basename(path))
    return title_string(base)


def path_to_slug(path, root=None):
    relative = path
    if root is not None:
        relative = os.path.relpath(path, root)
    target = remove_known_extension(relative)
    return slugify(target)


def convert_directory_recursive(directory, root):
    _print('Processing directory {0}'.format(os.path.relpath(directory, root)))

    node = {
        'name': path_to_title(directory),
        'id': path_to_slug(os.path.join(directory, 'index'), root),
        'children': []
    }

    files = files_in_directory_sorted(directory)

    index_path = find_index_file_in_directory(directory)

    if index_path is not None:
        _print('Found index {}'.format(index_path))
        node['html'] = file_to_html(index_path)
    else:
        _print('Autoindexing {}'.format(directory))
        node['html'] = auto_index(directory, root)
        node['autoindex'] = True

    for file in files:
        if os.path.isdir(file):
            node['children'].append(convert_directory_recursive(file, root))
        else:
            if not is_markdown_file(file):
                continue
            _print('Adding file {}'.format(file))
            node['children'].append({
                'name': path_to_title(file),
                'html': file_to_html(file),
                'id': path_to_slug(file, root)
            })

    return node


def build(root, target, title):
    if os.path.exists(target) and os.path.isfile(target):
        raise ExpectedDirectoryError(target)

    if not os.path.isdir(root):
        raise NotADirectoryError(root)

    if not os.path.isdir(target):
        mkdir_nested(target)

    root_node = convert_directory_recursive(root, root)

    root_node['name'] = title

    data = {
        'title': title,
        'tree': root_node
    }

    target_file = os.path.join(target, 'data.json')

    json.dump(data, open(target_file, 'w'))

    _print('Done: {0}'.format(target_file))
