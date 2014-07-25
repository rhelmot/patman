commands = [
        'init',
        'status',
        'add',
        'list',
        'swap',
        'help'
    ]

import sys, importlib

from . import manager

def main():
    if len(sys.argv) < 2:
        cmd('help')
    elif sys.argv[1] in commands:
        cmd(sys.argv[1], sys.argv[2:])
    elif len(sys.argv) < 3:
        cmd('help')
    elif sys.argv[2] in commands:
        repo = manager.resolve(sys.argv[1])
        cmd(sys.argv[2], sys.argv[3:], repo)
    else:
        cmd('help')

def cmd(name, args=[], repo=None):
    p_cmd = importlib.import_module(name)
    p_cmd.main(args, repo)

if __name__ == '__main__':
    main()
