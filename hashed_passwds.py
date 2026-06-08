import hashlib


def hash_passwd(password: str) -> str:
        hashed = hashlib.sha256(password.encode("utf-8")).hexdigest()
        return hashed