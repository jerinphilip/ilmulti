import sys
from io import StringIO


class Capturing:
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        del self._stringio  # free up some memory
        sys.stdout = self._stdout
