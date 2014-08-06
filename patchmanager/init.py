import manager
import os

def main(args, repo):
    if repo is not None:
        import help as p_help
        p_help.main(['init'])
        return 1

    try:
        manager.resolve()
        print 'No nested projects!'
        return 1
    except Exception:
        pass

    if not any(not x.startswith('.') for x in os.listdir('.')):
        raise Exception('Not initializing empty directory!')

    ppath = os.environ['PWD']
    phash = manager.shash(ppath)
    if len(args) < 1:
        args.append(raw_input("Give a name for this project: "))
    #if len(args) < 2:
    #    args.append(raw_input("Give the name of the executable for this project: "))
    # TODO: validate names
    #try:
    #    open(args[1])
    #except:
    #    print "Executable file doesn't exist!"
    #    print 'it was "%s"' % args[1]
    #    return 1

    cfgdir = os.path.join(manager.PATH, phash)
    os.mkdir(cfgdir)
    os.symlink(cfgdir, os.path.join(manager.PATH, args[0]))
    os.mkdir(os.path.join(cfgdir, 'snapshots'))
    os.mkdir(os.path.join(cfgdir, 'config'))
    open(os.path.join(cfgdir, 'config/destination'), 'w').write(ppath)
    repo = manager.Project(cfgdir)
    with repo.lock:
        #repo.set_executable(args[1])
        repo.set_ignores([])
        repo.snapshot('original')
        return 0
