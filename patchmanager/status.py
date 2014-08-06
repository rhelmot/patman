import manager

def main(args, repo):
    if repo is None: repo = manager.resolve()
    with repo.lock:
        if len(args) == 0:
            snap = repo.get_current_snapshot()
        else:
            snap = args[0]
            if not snap in zip(*repo.list_snapshots())[0]:
                print '%s is not a snapshot name!' % snap
                return 1
        diffs = repo.compare_snapshot(snap)
        if len(diffs) == 0 or (len(diffs) == 1 and diffs[0] == ''):
            print 'Using snapshot %s' % snap
            return 0
        else:
            print 'Using snapshot %s, with modifications:' % snap
            print '\n'.join(diffs)
            return 1
