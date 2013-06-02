
import hashlib, os

def singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance

def check_whitelist(params, whitelist):
    for name, value in params.items():
        if name not in whitelist:
            raise AssertionError('Some param is not whitelisted')

def check_mandatory(params, mustlist):
    for param in mustlist:
        if param not in params:
            raise AssertionError('Some required params are missed')

def int_param(param):
    try:
        return int(param)
    except Exception:
        raise AssertionError('Int param is not int')

def strn_param(param, max_length):
    try:
        res = str(param)
    except Exception:
        raise AssertionError('String param is not convertable to string')
    if len(res) > max_length:
        raise AssertionError('String param is too long')
    return res

def hash_password(password, salt):
    return hashlib.sha256(password.encode('utf-8') + salt.encode('utf-8')).hexdigest()

def generate_token():
    return hashlib.sha256(os.urandom(128)).hexdigest()