"""Cryptography and hashing utility library stubs."""

import hashlib


def compute_sha256(data: str) -> str:
    """Computes SHA-256 hash string for raw text."""
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def compute_md5(data: str) -> str:
    """Computes MD5 hash string for raw text."""
    return hashlib.md5(data.encode("utf-8")).hexdigest()
