#! /usr/bin/env python
# coding: utf-8

import os
import re
import click
import subprocess


def filetype_from_ext_and_header(filepath):
    path, filename = os.path.split(filepath)
    ext = os.path.splitext(filepath)[1]
    with open(filename, 'rb') as f:
        head = f.read(6)
        if re.match(r'.(J|j)(P|p)(E|e)?(G|g)', ext) and \
           re.match(rb'\xff\xd8', head):
            return 'jpg'
        elif re.match(r'.(P|p)(N|n)(G|g)', ext) and \
             re.match(rb'.PNG', head):
            return 'png'
        elif re.match(r'.(G|g)(I|i)(F|f)', ext) and \
             re.match(rb'GIF8(7|9)a', head):
            return 'gif'
        else:
            return 'not supported'


def is_command_exists(cmd):
    return 0 == subprocess.getstatusoutput('which {}'.format(cmd))[0]


def jpgopt(filepath, output, silent=False):
    cmd = 'jpegrescan'
    if not is_command_exists(cmd):
        print('{cmd} is not found in PATH.'.format(cmd=cmd))
        print('install {cmd} from {url}'.format(cmd=cmd, url='https://github.com/kud/jpegrescan'))
        return
        # raise FileNotFoundError('{cmd} is not found in PATH\n\n{url}'.format(cmd=cmd, url='https://github.com/kud/jpegrescan'))
    if silent:
        subprocess.run([cmd, '-q', filepath, output])
    else:
        print('using jpegrescan: optimize {} -> {}'.format(filepath, output))
        subprocess.run([cmd, filepath, output])


def pngopt(filepath, output, silent=False):
    cmd = 'pngquant'
    if not is_command_exists(cmd):
        print('{cmd} is not found in PATH.'.format(cmd=cmd))
        print('install {cmd} from {url}'.format(cmd=cmd, url='https://pngquant.org/'))
        return
        # raise FileNotFoundError('{cmd} is not found in PATH\n\n{url}'.format(cmd=cmd, url='https://pngquant.org/'))
    if silent:
        subprocess.run([cmd, filepath, '--output', output])
    else:
        print('using {cmd}: optimize {in_} -> {out}'.format(cmd=cmd, in_=filepath, out=output))
        subprocess.run([cmd, filepath, '--output', output])


@click.command()
@click.argument('filepath')
@click.option('--output', '-o', default=None)
@click.option('--silent', '-s', is_flag=True)
@click.option('--force', '-f', is_flag=True)
def optimize(filepath, output, silent, force):
    if output == None:
        output = os.path.splitext(filepath)[0] + '-opti' + os.path.splitext(filepath)[1]
    if force == False and os.path.exists(output):
        raise FileExistsError('output file {out} is already exists'.format(out=output))

    filetype = filetype_from_ext_and_header(filepath)
    if filetype == 'jpg':
        jpgopt(filepath, output, silent)
    elif filetype == 'png':
        pngopt(filepath, output, silent)
    elif filetype == 'gif':
        print('not supported yed.')
    else:
        print('check if the file is jpg/png/gif.')



def main():
    optimize()


if __name__ == '__main__':
    main()

