from __future__ import annotations

import os
import ssl

import certifi


def validate_ca_file(ca_file: str | None) -> None:
    if ca_file is not None and (not isinstance(ca_file, str) or not ca_file.strip()):
        raise ValueError("tls_ca_file must be a non-empty path to a CA PEM bundle")


def create_client_ssl_context(ca_file: str | None = None) -> ssl.SSLContext:
    """Verify against explicit CAs or certifi, without importing the Windows CA cache."""
    validate_ca_file(ca_file)
    if ca_file is not None:
        return ssl.create_default_context(cafile=ca_file)
    capath = os.getenv("SSL_CERT_DIR") or None
    if capath is not None and not os.path.isdir(capath):
        raise FileNotFoundError("SSL_CERT_DIR must point to an existing CA directory")
    return ssl.create_default_context(
        cafile=os.getenv("SSL_CERT_FILE") or (None if capath else certifi.where()),
        capath=capath,
    )
