import manager

def main(args, repo):
    if repo is None: repo = manager.resolve()
    csnap = repo.get_current_snapshot()
    for name, ctime in repo.list_snapshots():
        indic = '*' if csnap == name else ' '
        print '%20s %s %s' % (name, indic, ctime)
    repo.done()
    return 1
