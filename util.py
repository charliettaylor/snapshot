import hashlib
from typing import List

from config import settings


def contains(text: str, words: List[str], ignore_case=True):
    for word in words:
        if word in text:
            return True
        if ignore_case and word.lower() in text.lower():
            return True
    return False


def user_hash(username: str) -> str:
    combined_str = username + settings.hash_secret
    hash_obj = hashlib.md5()
    hash_obj.update(combined_str.encode("utf-8"))
    alphanumeric_hash = "".join(char for char in hash_obj.hexdigest() if char.isalnum())

    return alphanumeric_hash[:6]


def validate_username(username: str) -> bool:
    if len(username) > 15:
        return False
    return username.isalnum()
