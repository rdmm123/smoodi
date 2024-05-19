import random
import string
import re
import os
from typing import Dict, Any, Type

from flask import url_for, request


def load_from_env(cls: Type[Any]) -> Type[Any]:
    env_vars_to_load: dict[str, str] = getattr(cls, "load_from_env", {})
    for attribute, env_var in env_vars_to_load.items():
        value = os.getenv(env_var)

        if value is None:
            raise Exception(f"{env_var} not found in environment variables.")

        setattr(cls, attribute, value)
    return cls


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
