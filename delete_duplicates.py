import argparse

parser = argparse.ArgumentParser(
    description='delete duplicate files (based MD5-hashdigest)'
)
parser.add_argument(
    '--delete',
    action='store_true',
    help='set to delete actually. (default: dry-run)')
parser.add_argument(
    '-d', '--path',
    action='store',
    dest='path',
    type=str,
    help='set dir path. (default: .)')
args = parser.parse_args()

def get_file_names(dir_='.'):
    from os import scandir
    return sorted([f.name for f in scandir(dir_) if f.is_file()])

def remove_duplicate(filelist):
    from hashlib import md5
    from os import remove
    ret = set({})
    for f in filelist:
        digest = ''
        with open(f'{args.path}/{f}', 'rb') as fd:
            digest = md5(fd.read()).hexdigest()
        if digest in ret:
            if args.delete:
                print(f'delete: {f}')
                remove(f)
            else:
                print(f'delete(dry-run): {f}')
        else:
            ret.add(digest)

def main():
    fs = get_file_names(args.path)
    remove_duplicate(fs)

if __name__=='__main__':
    main()
