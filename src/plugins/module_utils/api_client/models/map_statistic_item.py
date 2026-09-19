from __future__ import annotations

from collections.abc import Generator, Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.simple_statistic_item import SimpleStatisticItem


T = TypeVar("T", bound="MapStatisticItem")


@_attrs_define
class MapStatisticItem:
    """
    Attributes:
        name (str | Unset): Item name
        type_ (str | Unset): Set to "MapStatisticItem"
        value (list[SimpleStatisticItem] | Unset): Named values
    """

    name: str | Unset = UNSET
    type_: str | Unset = UNSET
    value: list[SimpleStatisticItem] | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.simple_statistic_item import SimpleStatisticItem

        name = self.name

        type_ = self.type_

        value: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.value, Unset):
            value = []
            for value_item_data in self.value:
                value_item = value_item_data.to_dict()
                value.append(value_item)

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if type_ is not UNSET:
            field_dict["type"] = type_
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.simple_statistic_item import SimpleStatisticItem

        d = dict(src_dict)
        name = d.pop("name", UNSET)

        type_ = d.pop("type", UNSET)

        _value = d.pop("value", UNSET)
        value: list[SimpleStatisticItem] | Unset = UNSET
        if _value is not UNSET:
            value = []
            for value_item_data in _value:
                value_item = SimpleStatisticItem.from_dict(value_item_data)

                value.append(value_item)

        map_statistic_item = cls(
            name=name,
            type_=type_,
            value=value,
        )

        return map_statistic_item
