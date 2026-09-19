from __future__ import annotations

from collections.abc import Generator, Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, TextIO, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="Server")


@_attrs_define
class Server:
    """
    Attributes:
        type_ (str | Unset): Set to “Server”
        id (str | Unset): The id of the server, “localhost”
        daemon_type (str | Unset): “recursor” for the PowerDNS Recursor and “authoritative” for the Authoritative Server
        version (str | Unset): The version of the server software
        url (str | Unset): The API endpoint for this server
        config_url (str | Unset): The API endpoint for this server’s configuration
        zones_url (str | Unset): The API endpoint for this server’s zones
    """

    type_: str | Unset = UNSET
    id: str | Unset = UNSET
    daemon_type: str | Unset = UNSET
    version: str | Unset = UNSET
    url: str | Unset = UNSET
    config_url: str | Unset = UNSET
    zones_url: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        id = self.id

        daemon_type = self.daemon_type

        version = self.version

        url = self.url

        config_url = self.config_url

        zones_url = self.zones_url

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if type_ is not UNSET:
            field_dict["type"] = type_
        if id is not UNSET:
            field_dict["id"] = id
        if daemon_type is not UNSET:
            field_dict["daemon_type"] = daemon_type
        if version is not UNSET:
            field_dict["version"] = version
        if url is not UNSET:
            field_dict["url"] = url
        if config_url is not UNSET:
            field_dict["config_url"] = config_url
        if zones_url is not UNSET:
            field_dict["zones_url"] = zones_url

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        type_ = d.pop("type", UNSET)

        id = d.pop("id", UNSET)

        daemon_type = d.pop("daemon_type", UNSET)

        version = d.pop("version", UNSET)

        url = d.pop("url", UNSET)

        config_url = d.pop("config_url", UNSET)

        zones_url = d.pop("zones_url", UNSET)

        server = cls(
            type_=type_,
            id=id,
            daemon_type=daemon_type,
            version=version,
            url=url,
            config_url=config_url,
            zones_url=zones_url,
        )

        return server
