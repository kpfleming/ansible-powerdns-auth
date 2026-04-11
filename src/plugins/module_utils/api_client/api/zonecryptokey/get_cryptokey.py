from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.cryptokey import Cryptokey
from ...models.error import Error
from ...types import UNSET, Response


def _get_kwargs(
    server_id: str,
    zone_id: str,
    cryptokey_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/servers/{server_id}/zones/{zone_id}/cryptokeys/{cryptokey_id}".format(
            server_id=quote(str(server_id), safe=""),
            zone_id=quote(str(zone_id), safe=""),
            cryptokey_id=quote(str(cryptokey_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Cryptokey | Error:
    if response.status_code == 200:
        response_200 = Cryptokey.from_dict(response.json())

        return response_200

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Cryptokey | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    server_id: str,
    zone_id: str,
    cryptokey_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Cryptokey | Error]:
    """Returns all data about the CryptoKey, including the privatekey.

    Args:
        server_id (str):
        zone_id (str):
        cryptokey_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Cryptokey | Error]
    """

    kwargs = _get_kwargs(
        server_id=server_id,
        zone_id=zone_id,
        cryptokey_id=cryptokey_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    server_id: str,
    zone_id: str,
    cryptokey_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Cryptokey | Error | None:
    """Returns all data about the CryptoKey, including the privatekey.

    Args:
        server_id (str):
        zone_id (str):
        cryptokey_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Cryptokey | Error
    """

    return sync_detailed(
        server_id=server_id,
        zone_id=zone_id,
        cryptokey_id=cryptokey_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    server_id: str,
    zone_id: str,
    cryptokey_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Cryptokey | Error]:
    """Returns all data about the CryptoKey, including the privatekey.

    Args:
        server_id (str):
        zone_id (str):
        cryptokey_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Cryptokey | Error]
    """

    kwargs = _get_kwargs(
        server_id=server_id,
        zone_id=zone_id,
        cryptokey_id=cryptokey_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    server_id: str,
    zone_id: str,
    cryptokey_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Cryptokey | Error | None:
    """Returns all data about the CryptoKey, including the privatekey.

    Args:
        server_id (str):
        zone_id (str):
        cryptokey_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Cryptokey | Error
    """

    return (
        await asyncio_detailed(
            server_id=server_id,
            zone_id=zone_id,
            cryptokey_id=cryptokey_id,
            client=client,
        )
    ).parsed
