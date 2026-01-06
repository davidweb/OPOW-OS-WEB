"""
Local compatibility shim for django_cryptography.fields

This defines a minimal `encrypt` symbol so `from django_cryptography.fields import encrypt`
works when models import it. It is intentionally minimal: it returns the object unchanged
(whether used as a decorator or as a function wrapper). If you need actual field
encryption features, install a django_cryptography version compatible with your Django
or replace this shim with a fuller implementation.
"""

from functools import wraps
from typing import Any, Callable

def _is_callable(obj: Any) -> bool:
    return callable(obj)

def encrypt(obj: Any) -> Any:
    """
    Compatibility: return the object unchanged.

    Usage patterns handled:
    - As decorator: @encrypt on a Field class -> returns the class unchanged.
    - As wrapper: encrypt(models.CharField(...)) -> returns the field unchanged.

    If your code requires actual encryption behavior, replace this shim.
    """
    return obj

__all__ = ["encrypt"]
