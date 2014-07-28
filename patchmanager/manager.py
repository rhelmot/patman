import os, hashlib, datetime
from subprocess import Popen, PIPE
from lockfile import FileLock

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
        self.lock.acquire()
        self.cfg_executable = os.path.join(path, 'config/executable')
        self.cfg_ignores = os.path.join(path, 'config/ignores')
        self.cfg_cursnap = os.path.join(path, 'config/current_snapshot')
        self.client_dest = open(os.path.join(path, 'config/destination')).read()

    def done(self):
        self.lock.release()
        
    def snapshot(self, name):
        snapshot_path = os.path.join(self.cfgdir, 'snapshots', name)
        os.mkdir(snapshot_path)
        # This particular call uses globbing, needs os.system :/
        os.system('tar -czf "%s" -X "%s" -C "%s" *' % (
            os.path.join(snapshot_path, 'archive.tar.gz'),
            self.cfg_ignores,
            self.client_dest))
        Popen(['cp', self.cfg_executable, self.cfg_ignores, snapshot_path])
        self.set_current_snapshot(name)

    def restore(self, name):
        snapshot_path = os.path.join(self.cfgdir, 'snapshots', name)
        Popen(['tar', '-xf', os.path.join(snapshot_path, 'archive.tar.gz'),
            '-C', self.client_dest])
        Popen(['cp', 
            os.path.join(snapshot_path, 'executable'),
            os.path.join(snapshot_path, 'ignores'),
            self.cfgdir])
        self.set_current_snapshot(name)

    def set_executable(self, name):
        open(self.cfg_executable, 'w').write(name)

    def get_executable(self):
        return open(self.cfg_executable).read()

    def set_ignores(self, names):
        open(self.cfg_ignores, 'w').write('\n'.join(names))

    def get_ignores(self):
        return open(self.cfg_ignores).read().split('\n')

    def set_current_snapshot(self, name):
        open(self.cfg_cursnap, 'w').write(name)

    def get_current_snapshot(self):
        return open(self.cfg_cursnap).read()

    def list_snapshots(self):
        names = os.listdir(os.path.join(self.cfgdir, 'snapshots'))
        times = (datetime.datetime.fromtimestamp(os.path.getmtime(
            os.path.join(self.cfgdir, 'snapshots', x))) 
            for x in names)
        return sorted(zip(names, times), key=lambda x: x[1])

    def compare_snapshot(self, name):
        res = Popen(['tar', '-dzf', 
            os.path.join(self.cfgdir, 'snapshots', name, 'archive.tar.gz'),
            '-X', os.path.join(self.cfgdir, 'snapshots', name, 'ignores'),
            '-C', self.client_dest], 
            stdout=PIPE)
        return res.stdout.read().strip().split('\n')
