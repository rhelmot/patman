import manager

def main(args=[], repo=None):
    if repo is None: repo = manager.resolve()
    with repo.lock:
        repo.delete()
        return 0
