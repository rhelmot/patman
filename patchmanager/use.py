import manager

def main(args, repo):
    if repo is None: repo = manager.resolve()
    with repo.lock:
        if len(args) == 0:
            import help as p_help
            p_help.main(['use'])
            return 1
        if args[0] not in zip(*repo.list_snapshots())[0]:
            print 'Argument is not a snapshot name!'
            return 1
        repo.restore(args[0])
        return 0
