from . import corpus as C

directory = {}

def build_iitb():
    iitb_parallel = 'iitb-hi-en/parallel'
    iitb_mono = 'iitb-hi-en/mono'
    def get_path(tag, lang)
        return (os.path.join(iitb_parallel, 
                '{}.{}'.format(tag, lang)), lang)

    d = {}
    for tag in ["train", "dev", "test"]:
        first = get_path(tag, "en")
        second = get_path(tag, "hi")
        d[tag] = C.Parallel(first, second)

    return d

def build_wat():
    pass

directory["IITB"] = build_iitb()
