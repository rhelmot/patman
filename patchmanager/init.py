import manager
import os

def main(args, repo):
    if repo is not None:
        from . import help as p_help
        p_help.main(['init'])
        return

    try:
        manager.resolve()
        print 'No nested projects!'
        return
    except Exception:
        pass

    ppath = os.environ['PWD']
    phash = manager.shash(ppath)
    if len(args) < 1:
        args.append(raw_input("Give a name for this project: "))
    if len(args) < 2:
        args.append(raw_input("Give the name of the executable for this project: "))
    # TODO: validate names
    if not args[2] in os.listdir(ppath):
        raise Exception('Executable file doesn\'t exist!')

    cfgdir = os.path.join(manager.PATH, phash)
    os.mkdir(cfgdir)
    os.symlink(cfgdir, os.path.join(manager.PATH, args[0]))
    repo = manger.Project(cfgdir)
    repo.snapshot('original')

