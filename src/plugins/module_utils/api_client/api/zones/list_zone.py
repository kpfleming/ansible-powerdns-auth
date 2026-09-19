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
    zone_id: str,
    *,
    rrsets: bool | Unset = True,
    rrset_name: str | Unset = UNSET,
    rrset_type: str | Unset = UNSET,
    include_disabled: bool | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["rrsets"] = rrsets

    params["rrset_name"] = rrset_name

    params["rrset_type"] = rrset_type

    params["include_disabled"] = include_disabled

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/servers/{server_id}/zones/{zone_id}".format(
            server_id=quote(str(server_id), safe=""), zone_id=quote(str(zone_id), safe="")
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | Zone:
    if response.status_code == 200:
        response_200 = Zone.from_dict(response.json())

        return response_200

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
    zone_id: str,
    *,
    client: AuthenticatedClient | Client,
    rrsets: bool | Unset = True,
    rrset_name: str | Unset = UNSET,
    rrset_type: str | Unset = UNSET,
    include_disabled: bool | Unset = UNSET,
) -> Response[Error | Zone]:
    """zone managed by a server

    Args:
        server_id (str):
        zone_id (str):
        rrsets (bool | Unset):  Default: True.
        rrset_name (str | Unset):
        rrset_type (str | Unset):
        include_disabled (bool | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | Zone]
    """

    kwargs = _get_kwargs(
        server_id=server_id,
        zone_id=zone_id,
        rrsets=rrsets,
        rrset_name=rrset_name,
        rrset_type=rrset_type,
        include_disabled=include_disabled,
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
    rrsets: bool | Unset = True,
    rrset_name: str | Unset = UNSET,
    rrset_type: str | Unset = UNSET,
    include_disabled: bool | Unset = UNSET,
) -> Error | Zone | None:
    """zone managed by a server

    Args:
        server_id (str):
        zone_id (str):
        rrsets (bool | Unset):  Default: True.
        rrset_name (str | Unset):
        rrset_type (str | Unset):
        include_disabled (bool | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | Zone
    """

    return sync_detailed(
        server_id=server_id,
        zone_id=zone_id,
        client=client,
        rrsets=rrsets,
        rrset_name=rrset_name,
        rrset_type=rrset_type,
        include_disabled=include_disabled,
    ).parsed


async def asyncio_detailed(
    server_id: str,
    zone_id: str,
    *,
    client: AuthenticatedClient | Client,
    rrsets: bool | Unset = True,
    rrset_name: str | Unset = UNSET,
    rrset_type: str | Unset = UNSET,
    include_disabled: bool | Unset = UNSET,
) -> Response[Error | Zone]:
    """zone managed by a server

    Args:
        server_id (str):
        zone_id (str):
        rrsets (bool | Unset):  Default: True.
        rrset_name (str | Unset):
        rrset_type (str | Unset):
        include_disabled (bool | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | Zone]
    """

    kwargs = _get_kwargs(
        server_id=server_id,
        zone_id=zone_id,
        rrsets=rrsets,
        rrset_name=rrset_name,
        rrset_type=rrset_type,
        include_disabled=include_disabled,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    server_id: str,
    zone_id: str,
    *,
    client: AuthenticatedClient | Client,
    rrsets: bool | Unset = True,
    rrset_name: str | Unset = UNSET,
    rrset_type: str | Unset = UNSET,
    include_disabled: bool | Unset = UNSET,
) -> Error | Zone | None:
    """zone managed by a server

    Args:
        server_id (str):
        zone_id (str):
        rrsets (bool | Unset):  Default: True.
        rrset_name (str | Unset):
        rrset_type (str | Unset):
        include_disabled (bool | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | Zone
    """

    return (
        await asyncio_detailed(
            server_id=server_id,
            zone_id=zone_id,
            client=client,
            rrsets=rrsets,
            rrset_name=rrset_name,
            rrset_type=rrset_type,
            include_disabled=include_disabled,
        )
    ).parsed
