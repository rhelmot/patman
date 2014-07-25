import os, hashlib, datetime

CFGDIR = '.patman'
HOME = os.environ['HOME']
PATH = os.path.join(HOME, CFGDIR)

if not CFGDIR in os.listdir(HOME):
    os.mkdir(PATH)

def shash(s):
    n = hashlib.new('md5')
    n.update(s)
    return n.hexdigest()

def resolve(tag=None):
    if tag is None:
        pathkeys = list(os.path.split(os.environ['PWD']))
        while len(pathkeys) > 0:
            newpath = os.path.join(*pathkeys)
            pathhash = shash(newpath)
            if pathhash in os.listdir(PATH):
                return Project(os.path.join(PATH, pathhash))
            pathkeys.pop()
        raise Exception("No project name given and not in a project directory!")
    else:
        if tag not in os.listdir(PATH):
            raise Exception("No project named %s!" % tag)
        return Project(os.path.join(PATH, tag))

class Project:
    def __init__(self, path):
        self.cfgdir = path
        self.lock = FileLock(os.path.join(path, 'lock'))
        
    def snapshot(self, name):
        import random
        tempname = random.getrandbits(32)
        os.system('tar -czf /tmp/patman_%x.tar.gz *')
        os.system('mv /tmp/patmatn_%x.tar.gz "%s.tar.gz"' % (tempname, os.path.join(self.cfgdir, 'snapshots', name)))

    def list_snapshots(self):
        slist = os.listdir(os.path.join(self.cfgdir, 'snapshots'))
        out = [(x[:-7], datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(self.cfgdir, 'snapshots', x)))) for x in slist]
        return sorted(out, key=lambda x: x[1])

    def compare_snapshot(self, name):
        res = os.system('tar -dzf "%s.tar.gz" > /dev/null 2> /dev/null' % os.path.join(self.cfgdir, 'snapshots', name))
        return res == 0
