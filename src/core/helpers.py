import random
import string
import re
import os
from typing import Dict, Any

from flask import url_for, request


class LoadFromEnvMixin:
    load_from_env: Dict[str, str] = {}

    def __init__(self) -> None:
        self._load_attrs_from_env()

    def _load_attrs_from_env(self) -> None:
        for attribute, env_var in self.load_from_env.items():
            value = os.getenv(env_var)

            if value is None:
                raise Exception(f"{env_var} not found in environment variables.")

            setattr(self, attribute, value)


def get_random_string(length: int) -> str:
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def get_missing_keys(d: Dict[str, Any], *keys_to_check: str) -> list[str]:
    missing = []
    for key in keys_to_check:
        if key not in d or not d[key]:
            missing.append(key)

    return missing


def get_absolute_url_for(view: str) -> str:
    return request.host_url.rstrip("/") + url_for(view)


def is_email_valid(email: str) -> bool:
    match = re.match(r"^[\w\-\.]+@([\w\-]+\.)+[\w\-]{2,4}$", email)

    if match is None:
        return False

    return True


def truncate_text(text: str, max_length: int) -> str:
    return (text[:max_length] + "... (truncated)") if len(text) > max_length else text
