from __future__ import annotations

from collections.abc import Generator, Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.network import Network


T = TypeVar("T", bound="Networks")


@_attrs_define
class Networks:
    """
    Attributes:
        networks (list[Network] | Unset):
    """

    networks: list[Network] | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.network import Network

        networks: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.networks, Unset):
            networks = []
            for networks_item_data in self.networks:
                networks_item = networks_item_data.to_dict()
                networks.append(networks_item)

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if networks is not UNSET:
            field_dict["networks"] = networks

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.network import Network

        d = dict(src_dict)
        _networks = d.pop("networks", UNSET)
        networks: list[Network] | Unset = UNSET
        if _networks is not UNSET:
            networks = []
            for networks_item_data in _networks:
                networks_item = Network.from_dict(networks_item_data)

                networks.append(networks_item)

        return cls(
            networks=networks,
        )
