import pytest
from . import language_utils as lu

# Adding bunch of lazy-tests, just check a few cases.

_cases = {
    'injected': '__t2hi__ Hello World',
    'stripped': 'Hello World'
}

def test_canonicalize():
    assert(lu.canonicalize('ud') == 'ur')

def test_language_token():
    assert(lu.language_token('hi') == '__t2hi__')

def test_strip_language_token():
    assert(lu.strip_language_token(_cases['injected']) == _cases['stripped'])

def test_inject_token():
    injected = lu.inject_token([_cases['stripped']], tgt_lang='hi')
    assert(injected[0] == _cases['injected'])

def test_detect_lang_whole():
    result = lu.detect_lang('Hello World!')
    string, lang = result[0]
    assert(lang == 'en')

@pytest.mark.filterwarnings('ignore')
def test_detect_lang_splitted():
    result = lu.detect_lang('Hello World!', 'splitted')
    string, lang = result[0]
    assert(lang == 'en')

@pytest.mark.filterwarnings('ignore')
def test_detect_lang_unknown():
    result = lu.detect_lang('Hello World!', 'garbage')


