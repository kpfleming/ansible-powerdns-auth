from __future__ import annotations

from collections.abc import Generator, Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, TextIO, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="SimpleStatisticItem")


@_attrs_define
class SimpleStatisticItem:
    """
    Attributes:
        name (str | Unset): Item name
        value (str | Unset): Item value
    """

    name: str | Unset = UNSET
    value: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        value = self.value

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        name = d.pop("name", UNSET)

        value = d.pop("value", UNSET)

        simple_statistic_item = cls(
            name=name,
            value=value,
        )

        return simple_statistic_item
