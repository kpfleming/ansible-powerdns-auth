from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.view import View
from ...types import UNSET, Response


def _get_kwargs(
    server_id: str,
    view: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/servers/{server_id}/views/{view}".format(
            server_id=quote(str(server_id), safe=""), view=quote(str(view), safe="")
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | View:
    if response.status_code == 200:
        response_200 = View.from_dict(response.json())

        return response_200

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Error | View]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    server_id: str,
    view: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Error | View]:
    """List the contents of a given view

    Args:
        server_id (str):
        view (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | View]
    """

    kwargs = _get_kwargs(
        server_id=server_id,
        view=view,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    server_id: str,
    view: str,
    *,
    client: AuthenticatedClient | Client,
) -> Error | View | None:
    """List the contents of a given view

    Args:
        server_id (str):
        view (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | View
    """

    return sync_detailed(
        server_id=server_id,
        view=view,
        client=client,
    ).parsed


async def asyncio_detailed(
    server_id: str,
    view: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Error | View]:
    """List the contents of a given view

    Args:
        server_id (str):
        view (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | View]
    """

    kwargs = _get_kwargs(
        server_id=server_id,
        view=view,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    server_id: str,
    view: str,
    *,
    client: AuthenticatedClient | Client,
) -> Error | View | None:
    """List the contents of a given view

    Args:
        server_id (str):
        view (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | View
    """

    return (
        await asyncio_detailed(
            server_id=server_id,
            view=view,
            client=client,
        )
    ).parsed
