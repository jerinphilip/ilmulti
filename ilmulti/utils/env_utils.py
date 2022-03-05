import os


def resolve():
    if not "ILMULTI_DATA_ROOT" in os.environ:
        raise EnvironmentError("ILMULTI_DATA_ROOT not set.")

    ASSETS_DIR = os.environ["ILMULTI_DATA_ROOT"]
    if not os.path.exists(ASSETS_DIR):
        raise FileNotFoundError("Unable to find {}".format(ASSETS_DIR))

    return ASSETS_DIR
