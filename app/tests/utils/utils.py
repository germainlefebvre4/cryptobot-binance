import random
import string
import json
from datetime import date, time, datetime, timedelta

from typing import Dict

from fastapi.testclient import TestClient

from app.core.config import settings


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_int_range(start, end) -> int:
    return random.randint(start, end)


def random_float_range(start, end, precision=2) -> float:
    return round(random.uniform(start, end), precision)


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"
