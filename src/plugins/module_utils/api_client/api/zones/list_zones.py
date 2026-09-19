from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.zone import Zone
from ...types import UNSET, Response, Unset


def _get_kwargs(
    server_id: str,
    *,
    zone: str | Unset = UNSET,
    dnssec: bool | Unset = True,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["zone"] = zone

    params["dnssec"] = dnssec

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/servers/{server_id}/zones".format(server_id=quote(str(server_id), safe="")),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | list[Zone]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = Zone.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Error | list[Zone]]:
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
    zone: str | Unset = UNSET,
    dnssec: bool | Unset = True,
) -> Response[Error | list[Zone]]:
    """List all Zones in a server

    Args:
        server_id (str):
        zone (str | Unset):
        dnssec (bool | Unset):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | list[Zone]]
    """

    kwargs = _get_kwargs(
        server_id=server_id,
        zone=zone,
        dnssec=dnssec,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    server_id: str,
    *,
    client: AuthenticatedClient | Client,
    zone: str | Unset = UNSET,
    dnssec: bool | Unset = True,
) -> Error | list[Zone] | None:
    """List all Zones in a server

    Args:
        server_id (str):
        zone (str | Unset):
        dnssec (bool | Unset):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | list[Zone]
    """

    return sync_detailed(
        server_id=server_id,
        client=client,
        zone=zone,
        dnssec=dnssec,
    ).parsed


async def asyncio_detailed(
    server_id: str,
    *,
    client: AuthenticatedClient | Client,
    zone: str | Unset = UNSET,
    dnssec: bool | Unset = True,
) -> Response[Error | list[Zone]]:
    """List all Zones in a server

    Args:
        server_id (str):
        zone (str | Unset):
        dnssec (bool | Unset):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | list[Zone]]
    """

    kwargs = _get_kwargs(
        server_id=server_id,
        zone=zone,
        dnssec=dnssec,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    server_id: str,
    *,
    client: AuthenticatedClient | Client,
    zone: str | Unset = UNSET,
    dnssec: bool | Unset = True,
) -> Error | list[Zone] | None:
    """List all Zones in a server

    Args:
        server_id (str):
        zone (str | Unset):
        dnssec (bool | Unset):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | list[Zone]
    """

    return (
        await asyncio_detailed(
            server_id=server_id,
            client=client,
            zone=zone,
            dnssec=dnssec,
        )
    ).parsed
