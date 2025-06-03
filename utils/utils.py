import re


def Is_uuid(s):
    return bool(re.fullmatch(r"[0-9a-fA-F]{32}", s))
