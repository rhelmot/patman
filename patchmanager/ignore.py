import manager

def main(args, repo):
    if repo is None: repo = manager.resolve()
    if len(args) == 0:
        import help as p_help
        p_help.main(['ignore'])
        repo.done()
        return 1
    elif args[0] == 'list':
        print '\n'.join(repo.get_ignores())
    elif args[0] == 'remove':
        ignores = repo.get_ignores()
        for pattern in args[1:]:
            if not pattern in ignores:
                print 'Can\'t remove "%s" from ignores, not present' % pattern
            else:
                ignores.remove(pattern)
        repo.set_ignores(ignores)
    else:
        ignores = repo.get_ignores()
        ignores += args
        repo.set_ignores(ignores)
        
    repo.done()
    return 0
