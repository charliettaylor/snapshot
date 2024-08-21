from config import settings
import hashlib

def super_good_hash(username):
    combined_str = username + settings.hash_secret
    hash_obj = hashlib.md5()
    hash_obj.update(combined_str.encode('utf-8'))
    alphanumeric_hash = ''.join(char for char in hash_obj.hexdigest() if char.isalnum())[:6]
    
    return alphanumeric_hash
