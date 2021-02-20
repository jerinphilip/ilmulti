from collections import OrderedDict
import subprocess

def git_short():
    return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'])


SEMANTIC = OrderedDict([
    ('major',  0),
    ('minor',  2),
    ('patch',  0),
    ('suffix',  'alpha')
])


__version__ = '{major}.{minor}.{patch}-{suffix}'.format(**SEMANTIC.items())
