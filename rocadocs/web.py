import argparse
import os
import sys
import tarfile
import time
import urllib

from rocadocs.main import mkdir_nested

DIST_URL = 'https://raw.githubusercontent.com/rocadocs/web/master/dist/rocaweb.tar.gz'


def reporthook(count, block_size, total_size):
    global start_time
    if count == 0:
        start_time = time.time()
        return
    duration = time.time() - start_time
    progress_size = (count * block_size)
    speed = int(progress_size / (1024 * duration))
    percent = int(count * block_size * 100 / total_size)
    sys.stdout.write('\rGET %d%%, %d KB, %d KB/s, %d seconds passed' %
                     (percent, progress_size / 1024, speed, duration))
    sys.stdout.flush()


def main():
    parser = argparse.ArgumentParser(description='Install Rocadoc Web static content')
    parser.add_argument('--dir', help='directory to install to', type=str, required=True)

    args = parser.parse_args()

    dir = os.path.abspath(args.dir)
    targetfile = os.path.join(dir, 'rocaweb.tar.gz')

    print('Downloading {0} to {1}'.format(DIST_URL, targetfile))

    mkdir_nested(dir)

    try:
        urllib.urlretrieve(DIST_URL, targetfile, reporthook=reporthook)
    except IOError as e:
        print(e)
        return

    sys.stdout.write('\n')

    print('Unpacking')

    tar = tarfile.open(targetfile)
    tar.extractall(path=dir)
    tar.close()

    os.remove(targetfile)

    print('Done')
