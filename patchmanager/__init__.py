import init, status, ignore, list as p_list, use, snap, help as p_help, delete

commands = {
        'init': init,
        'status': status,
        'ignore': ignore,
        'list': p_list,
        'use': use,
        'snap': snap,
        'help': p_help,
        'delete': delete
        }

import sys
import manager

def main():
    if len(sys.argv) < 2:
        return cmd('help')
    elif sys.argv[1] in commands:
        return cmd(sys.argv[1], sys.argv[2:])
    elif len(sys.argv) < 3:
        return cmd('help')
    elif sys.argv[2] in commands:
        repo = manager.resolve(sys.argv[1])
        return cmd(sys.argv[2], sys.argv[3:], repo)
    else:
        return cmd('help')

def cmd(name, args=[], repo=None):
    p_cmd = commands[name]
    return p_cmd.main(args, repo)

if __name__ == '__main__':
    sys.exit(main())
