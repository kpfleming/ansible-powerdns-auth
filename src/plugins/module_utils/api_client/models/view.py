from __future__ import annotations

from collections.abc import Generator, Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="View")


@_attrs_define
class View:
    """
    Attributes:
        zones (list[str] | Unset): An array of zone names
    """

    zones: list[str] | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        zones: list[str] | Unset = UNSET
        if not isinstance(self.zones, Unset):
            zones = self.zones

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if zones is not UNSET:
            field_dict["zones"] = zones

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        zones = cast("list[str]", d.pop("zones", UNSET))

        view = cls(
            zones=zones,
        )

        return view
