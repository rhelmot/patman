import manager

def main(args, repo):
    if repo is None: repo = manager.resolve()
    if len(args) == 0:
        import help as p_help
        p_help.main(['snap'])
        repo.done()
        return 1
    if args[0] in zip(*repo.list_snapshots())[0]:
        print 'There is already a snapshot named "%s"!' % args[0]
        repo.done()
        return 1

    repo.snapshot(args[0])
    repo.done()
    return 0
