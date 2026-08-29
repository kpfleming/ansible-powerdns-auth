from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.tsig_key import TSIGKey
from ...types import UNSET, Response


def _get_kwargs(
    server_id: str,
    tsigkey_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/servers/{server_id}/tsigkeys/{tsigkey_id}".format(
            server_id=quote(str(server_id), safe=""), tsigkey_id=quote(str(tsigkey_id), safe="")
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | TSIGKey:
    if response.status_code == 200:
        response_200 = TSIGKey.from_dict(response.json())

        return response_200

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Error | TSIGKey]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    server_id: str,
    tsigkey_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Error | TSIGKey]:
    """Get a specific TSIGKeys on the server, including the actual key

    Args:
        server_id (str):
        tsigkey_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | TSIGKey]
    """

    kwargs = _get_kwargs(
        server_id=server_id,
        tsigkey_id=tsigkey_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    server_id: str,
    tsigkey_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Error | TSIGKey | None:
    """Get a specific TSIGKeys on the server, including the actual key

    Args:
        server_id (str):
        tsigkey_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | TSIGKey
    """

    return sync_detailed(
        server_id=server_id,
        tsigkey_id=tsigkey_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    server_id: str,
    tsigkey_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Error | TSIGKey]:
    """Get a specific TSIGKeys on the server, including the actual key

    Args:
        server_id (str):
        tsigkey_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | TSIGKey]
    """

    kwargs = _get_kwargs(
        server_id=server_id,
        tsigkey_id=tsigkey_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    server_id: str,
    tsigkey_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Error | TSIGKey | None:
    """Get a specific TSIGKeys on the server, including the actual key

    Args:
        server_id (str):
        tsigkey_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | TSIGKey
    """

    return (
        await asyncio_detailed(
            server_id=server_id,
            tsigkey_id=tsigkey_id,
            client=client,
        )
    ).parsed
