import os

ILMULTI_DIR = os.path.join(os.environ['HOME'], '.ilmulti')

# Handling a special case for supernova.
if 'HOSTNAME' in os.environ:
    if os.environ['HOSTNAME'] in ['fusor', 'supernova']:
        print("{hostname} detected. Switching. Please check if ok.".format(hostname=os.environ['HOSTNAME']))
        user = os.environ['USER']
        ILMULTI_DIR = os.path.join('/home/{user}'.format(user=user), '.ilmulti')

from .language_utils import canonicalize, language_token
from .download_utils import download_resources
from .language_utils import detect_lang
