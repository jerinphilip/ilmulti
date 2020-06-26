import os

ILMULTI_DIR = os.path.join(os.environ['HOME'], '.ilmulti')

from .language_utils import canonicalize, language_token
from .download_utils import download_resources
from .language_utils import detect_lang
