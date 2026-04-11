from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.cache_flush_result import CacheFlushResult
from ...models.error import Error
from ...types import UNSET, Response


def _get_kwargs(
    server_id: str,
    *,
    domain: str,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["domain"] = domain

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/servers/{server_id}/cache/flush".format(server_id=quote(str(server_id), safe="")),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CacheFlushResult | Error:
    if response.status_code == 200:
        response_200 = CacheFlushResult.from_dict(response.json())

        return response_200

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[CacheFlushResult | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    server_id: str,
    *,
    client: AuthenticatedClient | Client,
    domain: str,
) -> Response[CacheFlushResult | Error]:
    """Flush a cache-entry by name

    Args:
        server_id (str):
        domain (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CacheFlushResult | Error]
    """

    kwargs = _get_kwargs(
        server_id=server_id,
        domain=domain,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    server_id: str,
    *,
    client: AuthenticatedClient | Client,
    domain: str,
) -> CacheFlushResult | Error | None:
    """Flush a cache-entry by name

    Args:
        server_id (str):
        domain (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CacheFlushResult | Error
    """

    return sync_detailed(
        server_id=server_id,
        client=client,
        domain=domain,
    ).parsed


async def asyncio_detailed(
    server_id: str,
    *,
    client: AuthenticatedClient | Client,
    domain: str,
) -> Response[CacheFlushResult | Error]:
    """Flush a cache-entry by name

    Args:
        server_id (str):
        domain (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CacheFlushResult | Error]
    """

    kwargs = _get_kwargs(
        server_id=server_id,
        domain=domain,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    server_id: str,
    *,
    client: AuthenticatedClient | Client,
    domain: str,
) -> CacheFlushResult | Error | None:
    """Flush a cache-entry by name

    Args:
        server_id (str):
        domain (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CacheFlushResult | Error
    """

    return (
        await asyncio_detailed(
            server_id=server_id,
            client=client,
            domain=domain,
        )
    ).parsed
