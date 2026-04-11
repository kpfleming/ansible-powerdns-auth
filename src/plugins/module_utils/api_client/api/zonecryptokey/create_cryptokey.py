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
    *,
    body: Cryptokey,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/servers/{server_id}/zones/{zone_id}/cryptokeys".format(
            server_id=quote(str(server_id), safe=""), zone_id=quote(str(zone_id), safe="")
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Cryptokey | Error:
    if response.status_code == 201:
        response_201 = Cryptokey.from_dict(response.json())

        return response_201

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
    *,
    client: AuthenticatedClient | Client,
    body: Cryptokey,
) -> Response[Cryptokey | Error]:
    """Creates a Cryptokey

     This method adds a new key to a zone. The key can either be generated or imported by supplying the
    content parameter. if content, bits and algo are null, a key will be generated based on the default-
    ksk-algorithm and default-ksk-size settings for a KSK and the default-zsk-algorithm and default-zsk-
    size options for a ZSK.

    Args:
        server_id (str):
        zone_id (str):
        body (Cryptokey): Describes a DNSSEC cryptographic key

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Cryptokey | Error]
    """

    kwargs = _get_kwargs(
        server_id=server_id,
        zone_id=zone_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    server_id: str,
    zone_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: Cryptokey,
) -> Cryptokey | Error | None:
    """Creates a Cryptokey

     This method adds a new key to a zone. The key can either be generated or imported by supplying the
    content parameter. if content, bits and algo are null, a key will be generated based on the default-
    ksk-algorithm and default-ksk-size settings for a KSK and the default-zsk-algorithm and default-zsk-
    size options for a ZSK.

    Args:
        server_id (str):
        zone_id (str):
        body (Cryptokey): Describes a DNSSEC cryptographic key

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Cryptokey | Error
    """

    return sync_detailed(
        server_id=server_id,
        zone_id=zone_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    server_id: str,
    zone_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: Cryptokey,
) -> Response[Cryptokey | Error]:
    """Creates a Cryptokey

     This method adds a new key to a zone. The key can either be generated or imported by supplying the
    content parameter. if content, bits and algo are null, a key will be generated based on the default-
    ksk-algorithm and default-ksk-size settings for a KSK and the default-zsk-algorithm and default-zsk-
    size options for a ZSK.

    Args:
        server_id (str):
        zone_id (str):
        body (Cryptokey): Describes a DNSSEC cryptographic key

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Cryptokey | Error]
    """

    kwargs = _get_kwargs(
        server_id=server_id,
        zone_id=zone_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    server_id: str,
    zone_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: Cryptokey,
) -> Cryptokey | Error | None:
    """Creates a Cryptokey

     This method adds a new key to a zone. The key can either be generated or imported by supplying the
    content parameter. if content, bits and algo are null, a key will be generated based on the default-
    ksk-algorithm and default-ksk-size settings for a KSK and the default-zsk-algorithm and default-zsk-
    size options for a ZSK.

    Args:
        server_id (str):
        zone_id (str):
        body (Cryptokey): Describes a DNSSEC cryptographic key

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
            client=client,
            body=body,
        )
    ).parsed
