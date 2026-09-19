from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.config_setting import ConfigSetting
from ...models.error import Error
from ...types import UNSET, Response


def _get_kwargs(
    server_id: str,
    config_setting_name: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/servers/{server_id}/config/{config_setting_name}".format(
            server_id=quote(str(server_id), safe=""),
            config_setting_name=quote(str(config_setting_name), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ConfigSetting | Error:
    if response.status_code == 200:
        response_200 = ConfigSetting.from_dict(response.json())

        return response_200

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ConfigSetting | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    server_id: str,
    config_setting_name: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[ConfigSetting | Error]:
    """Returns a specific ConfigSetting for a single server

     NOT IMPLEMENTED

    Args:
        server_id (str):
        config_setting_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ConfigSetting | Error]
    """

    kwargs = _get_kwargs(
        server_id=server_id,
        config_setting_name=config_setting_name,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    server_id: str,
    config_setting_name: str,
    *,
    client: AuthenticatedClient | Client,
) -> ConfigSetting | Error | None:
    """Returns a specific ConfigSetting for a single server

     NOT IMPLEMENTED

    Args:
        server_id (str):
        config_setting_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ConfigSetting | Error
    """

    return sync_detailed(
        server_id=server_id,
        config_setting_name=config_setting_name,
        client=client,
    ).parsed


async def asyncio_detailed(
    server_id: str,
    config_setting_name: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[ConfigSetting | Error]:
    """Returns a specific ConfigSetting for a single server

     NOT IMPLEMENTED

    Args:
        server_id (str):
        config_setting_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ConfigSetting | Error]
    """

    kwargs = _get_kwargs(
        server_id=server_id,
        config_setting_name=config_setting_name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    server_id: str,
    config_setting_name: str,
    *,
    client: AuthenticatedClient | Client,
) -> ConfigSetting | Error | None:
    """Returns a specific ConfigSetting for a single server

     NOT IMPLEMENTED

    Args:
        server_id (str):
        config_setting_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ConfigSetting | Error
    """

    return (
        await asyncio_detailed(
            server_id=server_id,
            config_setting_name=config_setting_name,
            client=client,
        )
    ).parsed
