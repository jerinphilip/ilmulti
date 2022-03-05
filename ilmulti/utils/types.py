from typing import Literal, NewType

_langs = ["en", "hi", "ml", "bn", "ur", "ml", "ta", "te", "or", "pj", "gu", "mr"]
__Lang = Literal["en", "hi", "ml", "bn", "ur", "ml", "ta", "te", "or", "pj", "gu", "mr"]


class _Lang:
    """Either of: {}""".format(str(_langs))


Lang = _Lang()
Lang.__supertype__ = __Lang
