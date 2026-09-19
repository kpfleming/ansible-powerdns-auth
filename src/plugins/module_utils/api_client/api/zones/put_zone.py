from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.zone import Zone
from ...types import UNSET, Response


def _get_kwargs(
    server_id: str,
    zone_id: str,
    *,
    body: Zone,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/servers/{server_id}/zones/{zone_id}".format(
            server_id=quote(str(server_id), safe=""), zone_id=quote(str(zone_id), safe="")
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | Error:
    if response.status_code == 204:
        response_204 = cast("Any", None)
        return response_204

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | Error]:
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
    body: Zone,
) -> Response[Any | Error]:
    """Modifies basic zone data.

     The only fields in the zone structure which can be modified are: kind, masters, catalog, account,
    soa_edit, soa_edit_api, api_rectify, dnssec, and nsec3param. All other fields are ignored.

    Args:
        server_id (str):
        zone_id (str):
        body (Zone): This represents an authoritative DNS Zone.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
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
    body: Zone,
) -> Any | Error | None:
    """Modifies basic zone data.

     The only fields in the zone structure which can be modified are: kind, masters, catalog, account,
    soa_edit, soa_edit_api, api_rectify, dnssec, and nsec3param. All other fields are ignored.

    Args:
        server_id (str):
        zone_id (str):
        body (Zone): This represents an authoritative DNS Zone.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
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
    body: Zone,
) -> Response[Any | Error]:
    """Modifies basic zone data.

     The only fields in the zone structure which can be modified are: kind, masters, catalog, account,
    soa_edit, soa_edit_api, api_rectify, dnssec, and nsec3param. All other fields are ignored.

    Args:
        server_id (str):
        zone_id (str):
        body (Zone): This represents an authoritative DNS Zone.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
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
    body: Zone,
) -> Any | Error | None:
    """Modifies basic zone data.

     The only fields in the zone structure which can be modified are: kind, masters, catalog, account,
    soa_edit, soa_edit_api, api_rectify, dnssec, and nsec3param. All other fields are ignored.

    Args:
        server_id (str):
        zone_id (str):
        body (Zone): This represents an authoritative DNS Zone.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
    """

    return (
        await asyncio_detailed(
            server_id=server_id,
            zone_id=zone_id,
            client=client,
            body=body,
        )
    ).parsed
