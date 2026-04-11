from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.search_result_comment import SearchResultComment
from ...models.search_result_record import SearchResultRecord
from ...models.search_result_zone import SearchResultZone
from ...types import UNSET, Response, Unset


def _get_kwargs(
    server_id: str,
    *,
    q: str,
    max_: int,
    object_type: str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["q"] = q

    params["max"] = max_

    params["object_type"] = object_type

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/servers/{server_id}/search-data".format(server_id=quote(str(server_id), safe="")),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | list[SearchResultComment | SearchResultRecord | SearchResultZone]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for componentsschemas_search_results_item_data in _response_200:

            def _parse_componentsschemas_search_results_item(
                data: object,
            ) -> SearchResultComment | SearchResultRecord | SearchResultZone:
                try:
                    if not isinstance(data, dict):
                        raise TypeError
                    componentsschemas_search_result_type_0 = SearchResultZone.from_dict(data)

                    return componentsschemas_search_result_type_0
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError
                    componentsschemas_search_result_type_1 = SearchResultRecord.from_dict(data)

                    return componentsschemas_search_result_type_1
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                if not isinstance(data, dict):
                    raise TypeError
                componentsschemas_search_result_type_2 = SearchResultComment.from_dict(data)

                return componentsschemas_search_result_type_2

            componentsschemas_search_results_item = _parse_componentsschemas_search_results_item(
                componentsschemas_search_results_item_data
            )

            response_200.append(componentsschemas_search_results_item)

        return response_200

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Error | list[SearchResultComment | SearchResultRecord | SearchResultZone]]:
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
    q: str,
    max_: int,
    object_type: str | Unset = UNSET,
) -> Response[Error | list[SearchResultComment | SearchResultRecord | SearchResultZone]]:
    """Search the data inside PowerDNS

     Search the data inside PowerDNS for search_term and return at most max_results. This includes zones,
    records and comments. The * character can be used in search_term as a wildcard character and the ?
    character can be used as a wildcard for a single character.

    Args:
        server_id (str):
        q (str):
        max_ (int):
        object_type (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | list[SearchResultComment | SearchResultRecord | SearchResultZone]]
    """

    kwargs = _get_kwargs(
        server_id=server_id,
        q=q,
        max_=max_,
        object_type=object_type,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    server_id: str,
    *,
    client: AuthenticatedClient | Client,
    q: str,
    max_: int,
    object_type: str | Unset = UNSET,
) -> Error | list[SearchResultComment | SearchResultRecord | SearchResultZone] | None:
    """Search the data inside PowerDNS

     Search the data inside PowerDNS for search_term and return at most max_results. This includes zones,
    records and comments. The * character can be used in search_term as a wildcard character and the ?
    character can be used as a wildcard for a single character.

    Args:
        server_id (str):
        q (str):
        max_ (int):
        object_type (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | list[SearchResultComment | SearchResultRecord | SearchResultZone]
    """

    return sync_detailed(
        server_id=server_id,
        client=client,
        q=q,
        max_=max_,
        object_type=object_type,
    ).parsed


async def asyncio_detailed(
    server_id: str,
    *,
    client: AuthenticatedClient | Client,
    q: str,
    max_: int,
    object_type: str | Unset = UNSET,
) -> Response[Error | list[SearchResultComment | SearchResultRecord | SearchResultZone]]:
    """Search the data inside PowerDNS

     Search the data inside PowerDNS for search_term and return at most max_results. This includes zones,
    records and comments. The * character can be used in search_term as a wildcard character and the ?
    character can be used as a wildcard for a single character.

    Args:
        server_id (str):
        q (str):
        max_ (int):
        object_type (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | list[SearchResultComment | SearchResultRecord | SearchResultZone]]
    """

    kwargs = _get_kwargs(
        server_id=server_id,
        q=q,
        max_=max_,
        object_type=object_type,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    server_id: str,
    *,
    client: AuthenticatedClient | Client,
    q: str,
    max_: int,
    object_type: str | Unset = UNSET,
) -> Error | list[SearchResultComment | SearchResultRecord | SearchResultZone] | None:
    """Search the data inside PowerDNS

     Search the data inside PowerDNS for search_term and return at most max_results. This includes zones,
    records and comments. The * character can be used in search_term as a wildcard character and the ?
    character can be used as a wildcard for a single character.

    Args:
        server_id (str):
        q (str):
        max_ (int):
        object_type (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | list[SearchResultComment | SearchResultRecord | SearchResultZone]
    """

    return (
        await asyncio_detailed(
            server_id=server_id,
            client=client,
            q=q,
            max_=max_,
            object_type=object_type,
        )
    ).parsed
