import hashlib


def hash_this_string(some_string) -> int:
    hashable_string = (str(some_string)).encode()
    hex_digest = hashlib.sha1(hashable_string).hexdigest()
    return int(hex_digest, 16)
