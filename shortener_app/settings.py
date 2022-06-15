from datetime import datetime
from hashlib import sha256
from secrets import choice
from string import ascii_lowercase, ascii_uppercase, digits

MIN_KEY_LENGTH = 8
MAX_KEY_LENGTH = 50
DEFAULT_KEY_LENGTH = 8

MAX_URL_LENGTH = 500
MIN_URL_LENGTH = 1

DEFAULT_SALT_LENGTH = 10


def hasher(s: str) -> str:
    s = s.encode('utf-8')
    h = sha256(s)
    return h.hexdigest()


def date_time() -> str:
    dt = datetime.now().strftime('%D/%m/%Y %H:%M:%S.%f')
    return dt


def random_salt() -> str:
    s = ascii_uppercase + ascii_lowercase + digits
    r = ''.join([choice(s) for _ in range(DEFAULT_SALT_LENGTH)])
    return r
