import os
import sys
import tarfile
import shutil
import tempfile

try:
    from requests.utils import urlparse
    from requests import get as urlopen
    requests_available = True
except ImportError:
    requests_available = False
    if sys.version_info[0] == 2:
        from urlparse import urlparse  # noqa f811
        from urllib2 import urlopen  # noqa f811
    else:
        from urllib.request import urlopen
        from urllib.parse import urlparse

from . import ILMULTI_DIR

def _download_url_to_file(url, dst, hash_prefix=None, progress=True):

    # Reusing this from https://pytorch.org/docs/stable/_modules/torch/utils/model_zoo.html#load_url
    # With modifications.

    hash_prefix = None
    try:
        from tqdm import tqdm
    except ImportError:
        warnings.warn("Install tqdm to see download progress.")
        progress = None


    file_size = None
    if requests_available:
        u = urlopen(url, stream=True)
        if hasattr(u.headers, "Content-Length"):
            file_size = int(u.headers["Content-Length"])
        u = u.raw
    else:
        u = urlopen(url)
        meta = u.info()
        if hasattr(meta, 'getheaders'):
            content_length = meta.getheaders("Content-Length")
        else:
            content_length = meta.get_all("Content-Length")
        if content_length is not None and len(content_length) > 0:
            file_size = int(content_length[0])

    f = tempfile.NamedTemporaryFile(delete=False)
    try:
        if hash_prefix is not None:
            sha256 = hashlib.sha256()
        with tqdm(total=file_size, disable=not progress) as pbar:
            while True:
                buffer = u.read(8192)
                if len(buffer) == 0:
                    break
                f.write(buffer)
                if hash_prefix is not None:
                    sha256.update(buffer)
                pbar.update(len(buffer))

        f.close()
        if hash_prefix is not None:
            digest = sha256.hexdigest()
            if digest[:len(hash_prefix)] != hash_prefix:
                raise RuntimeError('invalid hash value (expected "{}", got "{}")'
                                   .format(hash_prefix, digest))
        shutil.move(f.name, dst)
    finally:
        f.close()
        if os.path.exists(f.name):
            os.remove(f.name)




def download_resources(url, filename, save_path=ILMULTI_DIR):
    if not os.path.exists(ILMULTI_DIR):
        os.makedirs(ILMULTI_DIR)
    fpath = os.path.join(ILMULTI_DIR, filename)
    _download_url_to_file(url, fpath)
    if tarfile.is_tarfile(fpath):
        shutil.unpack_archive(fpath, ILMULTI_DIR)
        os.remove(fpath)


