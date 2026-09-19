from __future__ import annotations

from collections.abc import Generator, Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, TextIO, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="AutoprimaryServer")


@_attrs_define
class AutoprimaryServer:
    """An autoprimary server that can provision new domains.

    Attributes:
        ip (str | Unset): IP address of the autoprimary server
        nameserver (str | Unset): DNS name of the autoprimary server
        account (str | Unset): Account name for the autoprimary server
    """

    ip: str | Unset = UNSET
    nameserver: str | Unset = UNSET
    account: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        ip = self.ip

        nameserver = self.nameserver

        account = self.account

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if ip is not UNSET:
            field_dict["ip"] = ip
        if nameserver is not UNSET:
            field_dict["nameserver"] = nameserver
        if account is not UNSET:
            field_dict["account"] = account

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        ip = d.pop("ip", UNSET)

        nameserver = d.pop("nameserver", UNSET)

        account = d.pop("account", UNSET)

        autoprimary_server = cls(
            ip=ip,
            nameserver=nameserver,
            account=account,
        )

        return autoprimary_server
