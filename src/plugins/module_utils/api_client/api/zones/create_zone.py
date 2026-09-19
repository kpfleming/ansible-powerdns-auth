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
    body: Zone,
    rrsets: bool | Unset = True,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["rrsets"] = rrsets

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/servers/{server_id}/zones".format(server_id=quote(str(server_id), safe="")),
        "params": params,
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | Zone:
    if response.status_code == 201:
        response_201 = Zone.from_dict(response.json())

        return response_201

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Error | Zone]:
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
    body: Zone,
    rrsets: bool | Unset = True,
) -> Response[Error | Zone]:
    """Creates a new domain, returns the Zone on creation.

    Args:
        server_id (str):
        rrsets (bool | Unset):  Default: True.
        body (Zone): This represents an authoritative DNS Zone.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | Zone]
    """

    kwargs = _get_kwargs(
        server_id=server_id,
        body=body,
        rrsets=rrsets,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    server_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: Zone,
    rrsets: bool | Unset = True,
) -> Error | Zone | None:
    """Creates a new domain, returns the Zone on creation.

    Args:
        server_id (str):
        rrsets (bool | Unset):  Default: True.
        body (Zone): This represents an authoritative DNS Zone.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | Zone
    """

    return sync_detailed(
        server_id=server_id,
        client=client,
        body=body,
        rrsets=rrsets,
    ).parsed


async def asyncio_detailed(
    server_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: Zone,
    rrsets: bool | Unset = True,
) -> Response[Error | Zone]:
    """Creates a new domain, returns the Zone on creation.

    Args:
        server_id (str):
        rrsets (bool | Unset):  Default: True.
        body (Zone): This represents an authoritative DNS Zone.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | Zone]
    """

    kwargs = _get_kwargs(
        server_id=server_id,
        body=body,
        rrsets=rrsets,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    server_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: Zone,
    rrsets: bool | Unset = True,
) -> Error | Zone | None:
    """Creates a new domain, returns the Zone on creation.

    Args:
        server_id (str):
        rrsets (bool | Unset):  Default: True.
        body (Zone): This represents an authoritative DNS Zone.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | Zone
    """

    return (
        await asyncio_detailed(
            server_id=server_id,
            client=client,
            body=body,
            rrsets=rrsets,
        )
    ).parsed
