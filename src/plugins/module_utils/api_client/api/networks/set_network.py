from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.set_network_body import SetNetworkBody
from ...types import UNSET, Response


def _get_kwargs(
    server_id: str,
    ip: str,
    prefixlen: str,
    *,
    body: SetNetworkBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/servers/{server_id}/networks/{ip}/{prefixlen}".format(
            server_id=quote(str(server_id), safe=""),
            ip=quote(str(ip), safe=""),
            prefixlen=quote(str(prefixlen), safe=""),
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
    ip: str,
    prefixlen: str,
    *,
    client: AuthenticatedClient | Client,
    body: SetNetworkBody,
) -> Response[Any | Error]:
    """Sets the view associated to the given network

    Args:
        server_id (str):
        ip (str):
        prefixlen (str):
        body (SetNetworkBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
    """

    kwargs = _get_kwargs(
        server_id=server_id,
        ip=ip,
        prefixlen=prefixlen,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    server_id: str,
    ip: str,
    prefixlen: str,
    *,
    client: AuthenticatedClient | Client,
    body: SetNetworkBody,
) -> Any | Error | None:
    """Sets the view associated to the given network

    Args:
        server_id (str):
        ip (str):
        prefixlen (str):
        body (SetNetworkBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
    """

    return sync_detailed(
        server_id=server_id,
        ip=ip,
        prefixlen=prefixlen,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    server_id: str,
    ip: str,
    prefixlen: str,
    *,
    client: AuthenticatedClient | Client,
    body: SetNetworkBody,
) -> Response[Any | Error]:
    """Sets the view associated to the given network

    Args:
        server_id (str):
        ip (str):
        prefixlen (str):
        body (SetNetworkBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
    """

    kwargs = _get_kwargs(
        server_id=server_id,
        ip=ip,
        prefixlen=prefixlen,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    server_id: str,
    ip: str,
    prefixlen: str,
    *,
    client: AuthenticatedClient | Client,
    body: SetNetworkBody,
) -> Any | Error | None:
    """Sets the view associated to the given network

    Args:
        server_id (str):
        ip (str):
        prefixlen (str):
        body (SetNetworkBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
    """

    return (
        await asyncio_detailed(
            server_id=server_id,
            ip=ip,
            prefixlen=prefixlen,
            client=client,
            body=body,
        )
    ).parsed
