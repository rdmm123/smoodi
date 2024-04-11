import random
import string
import os
from typing import Sequence, Dict, Any

from flask import url_for

def get_random_string(length: int):
    return ''.join(
        random.choices(string.ascii_letters + string.digits, k=length))

def get_missing_keys(d: Dict[str, Any], *keys_to_check: Sequence[str]):
    missing = []
    for key in keys_to_check:
        if key not in d or not d[key]:
            missing.append(key)

    return missing

def get_absolute_url_for(view: str):
    app_url = os.getenv('APP_URL')

    if not app_url:
        raise Exception("APP_URL environment variable not set.")
    
    return app_url.rstrip('/') + url_for(view)