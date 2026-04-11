from __future__ import annotations

from collections.abc import Generator, Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Literal, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="SearchResultZone")


@_attrs_define
class SearchResultZone:
    """
    Attributes:
        name (str | Unset):
        object_type (Literal['zone'] | Unset): set to "zone"
        zone_id (str | Unset):
    """

    name: str | Unset = UNSET
    object_type: Literal["zone"] | Unset = UNSET
    zone_id: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        object_type = self.object_type

        zone_id = self.zone_id

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if object_type is not UNSET:
            field_dict["object_type"] = object_type
        if zone_id is not UNSET:
            field_dict["zone_id"] = zone_id

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        name = d.pop("name", UNSET)

        object_type = cast("Literal['zone'] | Unset", d.pop("object_type", UNSET))
        if object_type != "zone" and not isinstance(object_type, Unset):
            raise ValueError(f"object_type must match const 'zone', got '{object_type}'")

        zone_id = d.pop("zone_id", UNSET)

        search_result_zone = cls(
            name=name,
            object_type=object_type,
            zone_id=zone_id,
        )

        return search_result_zone
