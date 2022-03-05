import subprocess
from collections import OrderedDict


def git_short():
    output = subprocess.check_output(["git", "rev-parse", "HEAD"])
    output = output.decode("utf-8").strip()
    return output


SEMANTIC = OrderedDict([("major", 0), ("minor", 2), ("patch", 0), ("suffix", "alpha")])

kwargs = dict(SEMANTIC.items())
__version__ = "{major}.{minor}.{patch}-{suffix}".format(**kwargs)
