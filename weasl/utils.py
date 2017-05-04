import os

def touch(path):
    with open(path, 'a'):
        os.utime(path, None)

def create_dir_structure(dir_structure):
    for branch in dir_structure:
        rest, node = os.path.split(branch)
        if not os.path.exists(rest):
            os.makedirs(rest)
        if not os.path.exists(branch):
            if '.' in node:
                touch(branch)
            else:
                os.mkdir(branch)
