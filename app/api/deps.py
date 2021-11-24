from typing import Generator

from app.cache.session import master as cache


def get_cache() -> Generator:
    try:
        yield cache
    finally:
        cache.close()