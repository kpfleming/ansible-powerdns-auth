from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.map_statistic_item import MapStatisticItem
from ...models.ring_statistic_item import RingStatisticItem
from ...models.statistic_item import StatisticItem
from ...types import UNSET, Response, Unset


def _get_kwargs(
    server_id: str,
    *,
    statistic: str | Unset = UNSET,
    includerings: bool | Unset = True,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["statistic"] = statistic

    params["includerings"] = includerings

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/servers/{server_id}/statistics".format(server_id=quote(str(server_id), safe="")),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | Error | list[MapStatisticItem | RingStatisticItem | StatisticItem]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:

            def _parse_response_200_item(
                data: object,
            ) -> MapStatisticItem | RingStatisticItem | StatisticItem:
                try:
                    if not isinstance(data, dict):
                        raise TypeError
                    response_200_item_type_0 = StatisticItem.from_dict(data)

                    return response_200_item_type_0
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError
                    response_200_item_type_1 = MapStatisticItem.from_dict(data)

                    return response_200_item_type_1
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                if not isinstance(data, dict):
                    raise TypeError
                response_200_item_type_2 = RingStatisticItem.from_dict(data)

                return response_200_item_type_2

            response_200_item = _parse_response_200_item(response_200_item_data)

            response_200.append(response_200_item)

        return response_200

    if response.status_code == 422:
        response_422 = cast("Any", None)
        return response_422

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | Error | list[MapStatisticItem | RingStatisticItem | StatisticItem]]:
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
    statistic: str | Unset = UNSET,
    includerings: bool | Unset = True,
) -> Response[Any | Error | list[MapStatisticItem | RingStatisticItem | StatisticItem]]:
    """Query statistics.

     Query PowerDNS internal statistics.

    Args:
        server_id (str):
        statistic (str | Unset):
        includerings (bool | Unset):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error | list[MapStatisticItem | RingStatisticItem | StatisticItem]]
    """

    kwargs = _get_kwargs(
        server_id=server_id,
        statistic=statistic,
        includerings=includerings,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    server_id: str,
    *,
    client: AuthenticatedClient | Client,
    statistic: str | Unset = UNSET,
    includerings: bool | Unset = True,
) -> Any | Error | list[MapStatisticItem | RingStatisticItem | StatisticItem] | None:
    """Query statistics.

     Query PowerDNS internal statistics.

    Args:
        server_id (str):
        statistic (str | Unset):
        includerings (bool | Unset):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error | list[MapStatisticItem | RingStatisticItem | StatisticItem]
    """

    return sync_detailed(
        server_id=server_id,
        client=client,
        statistic=statistic,
        includerings=includerings,
    ).parsed


async def asyncio_detailed(
    server_id: str,
    *,
    client: AuthenticatedClient | Client,
    statistic: str | Unset = UNSET,
    includerings: bool | Unset = True,
) -> Response[Any | Error | list[MapStatisticItem | RingStatisticItem | StatisticItem]]:
    """Query statistics.

     Query PowerDNS internal statistics.

    Args:
        server_id (str):
        statistic (str | Unset):
        includerings (bool | Unset):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error | list[MapStatisticItem | RingStatisticItem | StatisticItem]]
    """

    kwargs = _get_kwargs(
        server_id=server_id,
        statistic=statistic,
        includerings=includerings,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    server_id: str,
    *,
    client: AuthenticatedClient | Client,
    statistic: str | Unset = UNSET,
    includerings: bool | Unset = True,
) -> Any | Error | list[MapStatisticItem | RingStatisticItem | StatisticItem] | None:
    """Query statistics.

     Query PowerDNS internal statistics.

    Args:
        server_id (str):
        statistic (str | Unset):
        includerings (bool | Unset):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error | list[MapStatisticItem | RingStatisticItem | StatisticItem]
    """

    return (
        await asyncio_detailed(
            server_id=server_id,
            client=client,
            statistic=statistic,
            includerings=includerings,
        )
    ).parsed
