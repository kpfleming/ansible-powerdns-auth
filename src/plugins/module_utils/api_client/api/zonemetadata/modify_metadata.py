from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.metadata import Metadata
from ...types import UNSET, Response


def _get_kwargs(
    server_id: str,
    zone_id: str,
    metadata_kind: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/servers/{server_id}/zones/{zone_id}/metadata/{metadata_kind}".format(
            server_id=quote(str(server_id), safe=""),
            zone_id=quote(str(zone_id), safe=""),
            metadata_kind=quote(str(metadata_kind), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | Metadata:
    if response.status_code == 200:
        response_200 = Metadata.from_dict(response.json())

        return response_200

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Error | Metadata]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    server_id: str,
    zone_id: str,
    metadata_kind: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Error | Metadata]:
    """Replace the content of a single kind of domain metadata.

     Creates a set of metadata entries of given kind for the zone. Existing metadata entries for the zone
    with the same kind are removed.

    Args:
        server_id (str):
        zone_id (str):
        metadata_kind (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | Metadata]
    """

    kwargs = _get_kwargs(
        server_id=server_id,
        zone_id=zone_id,
        metadata_kind=metadata_kind,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    server_id: str,
    zone_id: str,
    metadata_kind: str,
    *,
    client: AuthenticatedClient | Client,
) -> Error | Metadata | None:
    """Replace the content of a single kind of domain metadata.

     Creates a set of metadata entries of given kind for the zone. Existing metadata entries for the zone
    with the same kind are removed.

    Args:
        server_id (str):
        zone_id (str):
        metadata_kind (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | Metadata
    """

    return sync_detailed(
        server_id=server_id,
        zone_id=zone_id,
        metadata_kind=metadata_kind,
        client=client,
    ).parsed


async def asyncio_detailed(
    server_id: str,
    zone_id: str,
    metadata_kind: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Error | Metadata]:
    """Replace the content of a single kind of domain metadata.

     Creates a set of metadata entries of given kind for the zone. Existing metadata entries for the zone
    with the same kind are removed.

    Args:
        server_id (str):
        zone_id (str):
        metadata_kind (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | Metadata]
    """

    kwargs = _get_kwargs(
        server_id=server_id,
        zone_id=zone_id,
        metadata_kind=metadata_kind,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    server_id: str,
    zone_id: str,
    metadata_kind: str,
    *,
    client: AuthenticatedClient | Client,
) -> Error | Metadata | None:
    """Replace the content of a single kind of domain metadata.

     Creates a set of metadata entries of given kind for the zone. Existing metadata entries for the zone
    with the same kind are removed.

    Args:
        server_id (str):
        zone_id (str):
        metadata_kind (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | Metadata
    """

    return (
        await asyncio_detailed(
            server_id=server_id,
            zone_id=zone_id,
            metadata_kind=metadata_kind,
            client=client,
        )
    ).parsed
