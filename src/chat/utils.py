from hashlib import md5 as _md5


def pair_uuid(a, b):
    a, b = (min((a, b)), max(a, b))
    return int(0.5 * (a + b) * (a + b + 1) + b)


def md5(a):
    return _md5(str(a).encode()).hexdigest()
