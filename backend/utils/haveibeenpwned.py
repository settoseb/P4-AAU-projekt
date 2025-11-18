import requests
import hashlib

def is_password_leaked(password: str) -> bool:
    hash = hashlib.sha1(password.encode()).hexdigest()
    hash_prefix = hash[:5]
    hash_suffix = hash[5:].upper()

    req = requests.get(f"https://api.pwnedpasswords.com/range/{hash_prefix}")

    if hash_suffix in req.text:
        return True
    else:
        return False