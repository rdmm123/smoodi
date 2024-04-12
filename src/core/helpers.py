import random
import string
import re
from typing import Dict, Any

from flask import url_for, request

def get_random_string(length: int) -> str:
    return ''.join(
        random.choices(string.ascii_letters + string.digits, k=length))

def get_missing_keys(d: Dict[str, Any], *keys_to_check: str) -> list[str]:
    missing = []
    for key in keys_to_check:
        if key not in d or not d[key]:
            missing.append(key)

    return missing

def get_absolute_url_for(view: str) -> str:
    return request.host_url.rstrip('/') + url_for(view)

def is_email_valid(email: str) -> bool:
    match = re.match(r'^[\w\-\.]+@([\w\-]+\.)+[\w\-]{2,4}$', email)

    if match is None:
        return False
    
    return True