from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.add_to_view_body import AddToViewBody
from ...models.error import Error
from ...types import UNSET, Response


def _get_kwargs(
    server_id: str,
    view: str,
    *,
    body: AddToViewBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/servers/{server_id}/views/{view}".format(
            server_id=quote(str(server_id), safe=""), view=quote(str(view), safe="")
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
    view: str,
    *,
    client: AuthenticatedClient | Client,
    body: AddToViewBody,
) -> Response[Any | Error]:
    """Adds a zone to a given view, creating it if needed

    Args:
        server_id (str):
        view (str):
        body (AddToViewBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
    """

    kwargs = _get_kwargs(
        server_id=server_id,
        view=view,
        body=body,
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
    body: AddToViewBody,
) -> Any | Error | None:
    """Adds a zone to a given view, creating it if needed

    Args:
        server_id (str):
        view (str):
        body (AddToViewBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
    """

    return sync_detailed(
        server_id=server_id,
        view=view,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    server_id: str,
    view: str,
    *,
    client: AuthenticatedClient | Client,
    body: AddToViewBody,
) -> Response[Any | Error]:
    """Adds a zone to a given view, creating it if needed

    Args:
        server_id (str):
        view (str):
        body (AddToViewBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
    """

    kwargs = _get_kwargs(
        server_id=server_id,
        view=view,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    server_id: str,
    view: str,
    *,
    client: AuthenticatedClient | Client,
    body: AddToViewBody,
) -> Any | Error | None:
    """Adds a zone to a given view, creating it if needed

    Args:
        server_id (str):
        view (str):
        body (AddToViewBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
    """

    return (
        await asyncio_detailed(
            server_id=server_id,
            view=view,
            client=client,
            body=body,
        )
    ).parsed
