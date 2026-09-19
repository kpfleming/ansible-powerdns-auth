from __future__ import annotations

from collections.abc import Generator, Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, TextIO, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="Network")


@_attrs_define
class Network:
    """
    Attributes:
        network (str | Unset): Network specification in human-readable form base address/prefix length
        view (str | Unset): The name of the view
    """

    network: str | Unset = UNSET
    view: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        network = self.network

        view = self.view

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if network is not UNSET:
            field_dict["network"] = network
        if view is not UNSET:
            field_dict["view"] = view

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        network = d.pop("network", UNSET)

        view = d.pop("view", UNSET)

        network = cls(
            network=network,
            view=view,
        )

        return network
