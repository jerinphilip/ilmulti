import pytest
from .io import ParallelWriter, ParallelReader
from .io import IOBase

def test_parallel_writer(tmp_path):
    with ParallelWriter(tmp_path, 'test_parallel', 'xx', 'yy') as writer:
        for src, tgt in zip(range(1, 100), range(2, 101)):
            writer.write(str(src), str(tgt))
    with ParallelReader(tmp_path, 'test_parallel', 'xx', 'yy') as reader:
        for src, tgt in reader:
            assert(int(src) + 1 == int(tgt))

def test_iobase_abstract_method(tmp_path):
    with pytest.raises(TypeError):
        iobase = IOBase(tmp_path, 'test_parallel', 'xx', 'yy')

    IOBase.__abstractmethods__ = ()
    iobase = IOBase(tmp_path, 'test_parallel', 'xx', 'yy')
    assert(iobase.fp() == None)

