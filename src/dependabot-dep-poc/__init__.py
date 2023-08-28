import pathlib


def get_bool_from_envvar(envvar: str) -> bool:
    """
    Returns a boolean from an envvar string. Returns True for any case-insensitive match of "True".
    """
    if envvar is None:
        return False
    if not isinstance(envvar, str):
        return False
    parsed_envvar = envvar.strip().lower()
    if parsed_envvar == "true":
        return True
    else:
        return False


__version__ = "2023.8.3"

VERSION = __version__
ROOT_DIR = pathlib.Path(__file__).absolute().parent

