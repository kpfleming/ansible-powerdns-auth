"""A client library for accessing PowerDNS Authoritative HTTP API"""

from .client import AuthenticatedClient, Client

__all__ = (
    "AuthenticatedClient",
    "Client",
)
