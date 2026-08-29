from __future__ import annotations

from collections.abc import Generator, Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, TextIO, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="SetNetworkBody")


@_attrs_define
class SetNetworkBody:
    """
    Attributes:
        view (str | Unset): The name of the view to use for this network
    """

    view: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        view = self.view

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if view is not UNSET:
            field_dict["view"] = view

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        view = d.pop("view", UNSET)

        set_network_body = cls(
            view=view,
        )

        return set_network_body
